# -*- coding: UTF-8 -*-
from django.shortcuts import render
from xiaoye.common import *
import WXBizMsgCrypt
import PIL.Image as Image, PIL.ImageFont as ImageFont, PIL.ImageDraw as ImageDraw
import re
import random


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
    if serviceName == 'raspTemp' or serviceName == 'rasp3Temp':
        filter = {}
        filter['checkedAt__gte'] = datetime.datetime.now() - datetime.timedelta(days=14)
        if serviceName == 'raspTemp':
            filter['model'] = 'B'
        elif serviceName == 'rasp3Temp':
            filter['model'] = '3B'
        date = []
        data = []
        for rt in RaspTemperature.objects.filter(**filter).all():
            date.append(timezone.localtime(rt.checkedAt).strftime("%Y-%m-%d %H:%M:%S"))
            data.append(rt.temperature)
        result['date'] = date
        result['data'] = data
    elif serviceName == 'roomTempHum':
        filter = {}
        filter['checkedAt__gte'] = datetime.datetime.now() - datetime.timedelta(days=14)
        dateList = []
        tempList = []
        humList = []
        for rt in RoomTemp.objects.filter(**filter).all():
            dateList.append(timezone.localtime(rt.checkedAt).strftime("%Y-%m-%d %H:%M:%S"))
            tempList.append(rt.temperature)
            humList.append(rt.humidity)
        result['date'] = dateList
        result['temp'] = tempList
        result['hum'] = humList
    elif serviceName == 'mlp':
        inputLocDict = {}
        hiddenLocDict = {}
        outputLocDict = {}
        nodeList = []
        linkList = []

        m = InputValue.objects.all().count()
        for n in range(m):
            model = InputValue.objects.all()[n]
            inputLocDict[model.id] = n
            nodeList.append({
                "name": model.value,
                "value": 0.,
                "category": 0
            })
        k = HiddenNode.objects.all().count()
        for n in range(k):
            model = HiddenNode.objects.all()[n]
            hiddenLocDict[model.id] = n + m
            nodeList.append({
                "name": model.hiddenKey,
                "value": 0,
                "category": 1
            })
        for n in range(OutputValue.objects.all().count()):
            model = OutputValue.objects.all()[n]
            outputLocDict[model.id] = n + m + k
            nodeList.append({
                "name": model.value,
                "value": 0,
                "category": 2
            })
        # print nodeList

        for model in InputHiddenMapping.objects.all():
            source = inputLocDict[model.inputValue.id]
            target = hiddenLocDict[model.hiddenNode.id]
            weight = model.weight * 5.0
            linkList.append({
                "source": source,
                "target": target,
                "lineStyle": {
                    "normal": {
                        "color": "#cac",
                        "width": weight,
                        "curveness": 0.2
                    }
                }
            })

        for model in HiddenOutputMapping.objects.all():
            source = hiddenLocDict[model.hiddenNode.id]
            target = outputLocDict[model.outputValue.id]
            weight = model.weight * 5.0
            linkList.append({
                "source": source,
                "target": target,
                "lineStyle": {
                    "normal": {
                        "color": "#acc",
                        "width": weight,
                        "curveness": 0.2
                    }
                }
            })
        # print linkList

        result = {
            "type": "force",
            "categories": [
                {
                    "name": u"输入"
                    ,
                    # "keyword": {},
                    # "base": "Input"
                },
                {
                    "name": u"隐藏"
                    # ,
                    # "keyword": {},
                    # "base": "Hidden"
                },
                {
                    "name": u"输出"
                    # ,
                    # "keyword": {},
                    # "base": "Output"
                }
            ],
            "nodes": nodeList,
            "links": linkList
        }

    else:
        return ResponseObject(1, u'Invalid parameter').toJSONHttpResponse()
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
    elif serviceName == 'recordTempHum' and serviceData:
        temp = serviceData.get('temp', 0)
        hum = serviceData.get('hum', 0)
        rt = RoomTemp()
        rt.temperature = temp
        rt.humidity = hum
        rt.save()
        return ResponseObject(0).toJSONHttpResponse()
    return ResponseObject(1, u'Error').toJSONHttpResponse()


def genImageFromText(text, imageName):
    actLength = 0
    lines = []
    j = 0
    subline = []
    for i in range(len(text)):
        j = j + 1
        if re.match('[\\w\\s\\d]', text[i]):
            actLength = actLength + 1
        else:
            actLength = actLength + 2
        subline.append(text[i])
        if actLength % 14 == 0:
            lines.append(''.join(subline))
            subline = []
    if subline:
        lines.append(''.join(subline))
    height = len(lines) * 80
    im = Image.new("RGB", (360, height), (205, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype("./xiaoye/MSYHBD.TTF", 50)
    y = 0
    for l in lines:
        dr.text((10, 5 + y), l, font=font, fill="#4e6cb4")
        y = y + 80
    im.show()
    im.save(imageName)


@csrf_exempt
def weixin_func(request):
    """
    Used for weixin public platform call back. -> mp.weixin.qq.com
    When user followed, save user openId in our table

    :param request:
    :return:
    """
    log.info('request %s' % request.GET)
    log.info('request body %s' % request.body)
    responseXML = None
    wc = WebChat(settings.WECHAT_TOKEN)
    if wc.isValid(request):
        if wc.validateSignature(request):
            return HttpResponse(request.GET.get('echostr', ''))
        else:
            return HttpResponse(u'你这么帅，赶紧从我面前消失')
    xml = request.body
    if not xml:
        return HttpResponse(u'你这么帅，赶紧从我面前消失')
    root = ElementTree.XML(xml)
    xmldict = XmlDictConfig(root)
    toUserName = xmldict.get('ToUserName', None)
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
    fromUserName = xmldict.get('FromUserName', None)
    msgType = xmldict.get('MsgType', None)
    event = xmldict.get('Event', None)
    eventKey = xmldict.get('EventKey', None)
    createTime = xmldict.get('CreateTime', None)
    msgId = xmldict.get('MsgId', None)
    content = xmldict.get('Content', None)
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
    else:
        wu = wu[0]
    try:
        m = WeixinMsg()
        m.fromUser = wu
        m.createTime = createTime
        m.content = content
        m.msgType = msgType
        m.msgId = msgId
        m.event = event
        m.eventKey = eventKey
        m.save()
    except Exception, e:
        log.error(e.message)
    filename = random.randint(1, 999)
    log.info('%d', filename)
    filename = '%s%s' % (fromUserName, filename)
    filename = hashlib.md5(filename).hexdigest()
    path = 'http://xiaoyexu.iok.la/static/%s.jpg' % filename
    genImageFromText(content, './static/%s.jpg' % filename)
    messageResponse = """您的山寨大字已经准备好 <a href="%s">在这里</a>""" % path
    responseXML = wc.returnTextResponse(fromUserName, toUserName, messageResponse)
    if msgType == 'event':
        if event == 'CLICK':
            pass
        elif event == 'subscribe':
            responseXML = wc.returnTextResponse(fromUserName, toUserName, u'终于等到你')
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

    if not responseXML:
        responseXML = wc.returnTextResponse(fromUserName, toUserName, u'收到')
    return HttpResponse(responseXML)


@csrf_exempt
def weixin(request):
    try:
        return weixin_func(request)
    except Exception, e:
        log.error(e.message)
        return HttpResponse('')
