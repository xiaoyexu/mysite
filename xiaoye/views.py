# -*- coding: UTF-8 -*-
from django.shortcuts import render
from xiaoye.common import *
import WXBizMsgCrypt

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


@csrf_exempt
@requireWebProcess(need_login=False)
def ajax(request):
    serviceName = request.GET.get('sn', None)
    result = {}
    filter = {}
    filter['checkedAt__gte'] = datetime.datetime.now() - datetime.timedelta(days=14)
    if serviceName == 'raspTemp':
        filter['model'] = 'B'
    elif serviceName == 'rasp3Temp':
        filter['model'] = '3B'
    else:
        return ResponseObject(1, u'Invalid parameter').toJSONHttpResponse()
    date = []
    data = []
    for rt in RaspTemperature.objects.filter(**filter).all():
        date.append(timezone.localtime(rt.checkedAt).strftime("%Y-%m-%d %H:%M:%S"))
        data.append(rt.temperature)
    result['date'] = date
    result['data'] = data
    return HttpResponse(json.dumps(result))


@csrf_exempt
@requireJSONAPIProcess(need_login=True, need_decrypt=True)
def rs(request):
    serviceName = request.dictBody.get('sn', None)
    serviceData = request.dictBody.get('sd', None)
    if serviceName == 'recordRaspTemp' and serviceData:
        temp = serviceData.get('temp', 0)
        model = serviceData.get('model', None)
        rt = RaspTemperature()
        rt.temperature = temp
        rt.model = model
        rt.save()
        return ResponseObject(0).toJSONHttpResponse()
    return ResponseObject(1, u'Error').toJSONHttpResponse()


@csrf_exempt
def weixin(request):
    """
    Used for weixin public platform call back. -> mp.weixin.qq.com
    When user followed, save user openId in our table

    :param request:
    :return:
    """
    log.info('request %s' % request.GET)
    log.info('request body %s' % request.body)
    wc = WebChat(settings.WECHAT_TOKEN)
    if wc.isValid(request) and wc.validateSignature(request):
        return HttpResponse(request.GET.get('echostr', ''))
    xml = request.body
    root = ElementTree.XML(xml)
    xmldict = XmlDictConfig(root)
    toUserName = xmldict.get('ToUserName', None)
    fromUserName = xmldict.get('FromUserName', None)
    encryptContent = xmldict.get('Encrypt', None)
    wxAppId = getSystemConfigByKey('WX_APPID')['value1']
    wxSecret = getSystemConfigByKey('WX_SECRET')['value1']
    wxToken = getSystemConfigByKey('WX_TOKEN')['value1']
    wxAESKey = getSystemConfigByKey('WX_AES_KEY')['value1']
    if encryptContent:
        decrypt_test = WXBizMsgCrypt.WXBizMsgCrypt(wxToken, wxAESKey, wxAppId)
        msg_signature = request.GET.get('msg_signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        ret, decryp_xml = decrypt_test.DecryptMsg(xml, msg_signature, timestamp, nonce)
        log.info('%s %s' % (ret, decryp_xml))
        root = ElementTree.XML(decryp_xml)
        xmldict = XmlDictConfig(root)
    msgType = xmldict.get('MsgType', None)
    event = xmldict.get('Event', None)
    eventKey = xmldict.get('EventKey', None)
    createTime = xmldict.get('CreateTime', None)
    msgId = xmldict.get('MsgId', None)
    content = xmldict.get('Content', None)
    try:
        m = WeixinMsg()
        m.fromUserName = fromUserName
        m.createTime = createTime
        m.content = content
        m.msgType = msgType
        m.msgId = msgId
        m.save()
    except Exception, e:
        log.error(e.message)
    if msgType == 'event':
        if event == 'CLICK':
            pass
    # Store token and if expired, get lastest one
    wxAccessTokenConf = getSystemConfigByKey('WX_ACCESS_TOKEN')
    wxAccessTokenExpConf = getSystemConfigByKey('WX_ACCESS_TOKEN_EXPIRE')
    wxAccessToken = wxAccessTokenConf.get('value1', None) if wxAccessTokenConf else None
    isExpired = False
    if wxAccessTokenExpConf:
        expireDate = datetime.datetime.strptime(wxAccessTokenExpConf['value1'], '%Y-%m-%d %H:%M:%S')
        isExpired = datetime.datetime.now() > expireDate
    if not wxAccessTokenConf or isExpired:
        result = getWXToken(wxAppId, wxSecret)
        r = json.loads(result)
        token = r.get('access_token', None)
        expires_in = r.get('expires_in', None)
        setSystemConfigByKey('WX_ACCESS_TOKEN', {'value1': token})
        setSystemConfigByKey('WX_ACCESS_TOKEN_EXPIRE',
                             {'value1': (datetime.datetime.now() + datetime.timedelta(seconds=expires_in)).strftime(
                                 '%Y-%m-%d %H:%M:%S')})
        wxToken = token
    log.info('valid token %s' % wxToken)
    log.info('from user %s' % fromUserName)
    # Check and save user openId
    wu = WeixinUser.objects.filter(wxOpenId=fromUserName)
    if not wu:
        # If user info API granted
        # log.info('No user data')
        # url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN'
        # url = url % (wxToken, fromUserName)
        # headers = {}
        # headers['Content-Type'] = 'application/json'
        # (code, reason, result) = sendRequest(url, headers, None)
        # log.info('%s' % result)
        # jsonResult = json.loads(result)
        # errcode = jsonResult.get('errcode', None)
        # if errcode:
        #     log.info('Error %s' % errcode)
        # else:
        #     wu = WeixinUser()
        #     wu.wxOpenId = jsonResult['openid']
        #     wu.wxUnionid = jsonResult['unionid']
        #     wu.wxName = jsonResult['nickname']
        #     wu.save()
        wu = WeixinUser()
        wu.wxOpenId = fromUserName
        wu.save()
    responseXML = wc.returnTextResponse(fromUserName, toUserName, u'收到')
    return HttpResponse(responseXML)
