# -*- coding: UTF-8 -*-
from django.shortcuts import render
from xiaoye.common import *


@csrf_exempt
@requireJSONAPIProcess(need_login=False, need_decrypt=False)
def jsonResult(request):
    ro = ResponseObject(0, u'')
    return ro.toJSONHttpResponse()


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
