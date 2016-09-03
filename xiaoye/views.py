# -*- coding: UTF-8 -*-
from django.shortcuts import render
from xiaoye.common import *


##### JSON API #####

@csrf_exempt
@requireJSONAPIProcess(need_login=False, need_decrypt=False)
def jsonResult(request):
    ro = ResponseObject(0, u'')
    return ro.toJSONHttpResponse()


# Login
def api_login(request):
    body = request.dictBody
    username = body.get('username', None)
    password = body.get('password', None)
    user = User.objects.filter(loginName=username)
    if not user:
        # User not found
        return ResponseObject(1, u'登录失败')
    user = user[0]
    if not user.loginCredentialEncrypted:
        # User login credential is not encrypted, encrypted it by sha1
        user.loginCredential = hashlib.sha1(user.loginCredential).hexdigest()
        user.loginCredentialEncrypted = True
        user.save()
    if user.loginCredential != password:
        return ResponseObject(2, u'登录失败')
    if user.status.key != 'ACTIVE':
        return ResponseObject(3, u'登录失败')
    if not request.need_decrypt:
        request.session['userId'] = '%s' % user.userId
    return ResponseObject(0, data={'userId': '%s' % user.userId})


@csrf_exempt
@requireJSONAPIProcess(need_login=False, need_decrypt=False)
def apiLogin(request):
    return api_login(request).toJSONHttpResponse()


##### Web view #####

@requireWebProcess(need_login=False)
def index(request):
    # return webSite.handle(request)
    return THR(request, 'xiaoye/index.html', {})


@requireWebProcess(need_login=False)
def back(request):
    navPath = request.session.get('navPath', [])
    request.method = 'GET'
    if len(navPath) >= 3:
        # Last request is back, navPath[-1]
        # User last accessed request is navPath[-2]
        # So back to navPath[-3] and remove last 2 item
        navPath = navPath[:-2]
        view_func = navPath[-1]
        request.session['navPath'] = navPath
        return eval(view_func)(request)
    else:
        return index(request)


@requireWebProcess(need_login=False)
def logoff(request):
    for k, v in request.session.items():
        del request.session[k]
    response = HttpResponseRedirect('index')
    return response


@requireWebProcess(need_login=False)
def app1_1(request):
    return THR(request, 'xiaoye/app1_1.html', {})


@requireWebProcess(need_login=False)
def app1_2(request):
    return THR(request, 'xiaoye/app1_2.html', {})


@requireWebProcess(need_login=False)
def app2_1(request):
    return THR(request, 'xiaoye/app2_1.html', {})


@requireWebProcess(need_login=False)
@csrf_exempt
def ajax(request):
    serviceName = request.GET.get('sn', None)
    result = {}
    if serviceName == 'raspTemp':
        date = []
        data = []
        for rt in RaspTemperature.objects.filter(checkedAt__gte=datetime.datetime.now() - datetime.timedelta(days=14)).all():
            date.append(timezone.localtime(rt.checkedAt).strftime("%Y-%m-%d %H:%M:%S"))
            data.append(rt.temperature)
        result['date'] = date
        result['data'] = data
    return HttpResponse(json.dumps(result))
