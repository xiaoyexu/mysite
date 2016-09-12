# -*- coding: UTF-8 -*-
__author__ = 'xuxiaoye'

import smtplib
import email
from email.mime.text import MIMEText
from models import *
import ssl
import urllib
import urllib2
import json
import logging
import pyDes
import base64
import hashlib
import datetime
import xml.etree.ElementTree as ElementTree
import re
import bs4
import urlparse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone

log = logging.getLogger('default')

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden, \
    HttpResponseNotFound
from django.template import RequestContext, loader


class ResponseObject(object):
    """
    A Response object to store code description and data of any dictionary or array
    """

    def __init__(self, code, desc='', data=None):
        if code == 0:
            desc = 'success'
        if data is None:
            data = {}
        self.code = code
        self.desc = desc
        self.data = data

    def toJSONHttpResponse(self):
        """
        Convert to JSON response text

        :return: String of json
        """
        return HttpResponse(json.dumps(self.getJSONDict()))

    def getJSONDict(self):
        """
        Convert to dictionary

        :return: A dictionary of response
        """
        return {'code': self.code, 'desc': self.desc, 'data': self.data}


def THR(request, template, context):
    """
    Return Django HttpResponse with given template and context

    :param request:
    :param template:
    :param context:
    :return:
    """
    template = loader.get_template(template)
    ctx = RequestContext(request, context)
    return HttpResponse(template.render(ctx))


def decrypt(text, dec=True):
    """
    Decrypt text by 3DES.

    :param text: Text to be decrypted
    :param dec: Whether to decrypted, may return original text if False
    :return: A decrypted text, or original text if no decryption needed
    """
    if dec:
        try:
            # 3DES key
            key = settings.API_3DES_KEY
            # 3DES Initial vector
            iv = settings.API_3DES_IV
            # No padding
            pad = None
            # 3DES object
            des = pyDes.triple_des(key, pyDes.CBC, iv, pad, pyDes.PAD_PKCS5)
            text = base64.decodestring(text)
            decryptStr = des.decrypt(text, pad, pyDes.PAD_PKCS5)
        except Exception, e:
            log.error(e.message)
            decryptStr = ''
        return decryptStr
    else:
        return text


def encrypt(text):
    try:
        # 3DES key
        key = settings.API_3DES_KEY
        # 3DES Initial vector
        iv = settings.API_3DES_IV
        # No padding
        pad = None
        # 3DES object
        des = pyDes.triple_des(key, pyDes.CBC, iv, pad, pyDes.PAD_PKCS5)
        # Encrytp
        encryptStr = des.encrypt(text, pad, pyDes.PAD_PKCS5)
        # Then base64
        encryptStr = base64.encodestring(encryptStr)
    except Exception, e:
        log.error(e.message)
        encryptStr = ''
    return encryptStr


def requireJSONAPIProcess(need_login=True, need_decrypt=True):
    """
    Decoration for preprocess of each request.

    Parameter need_login, need_decrypt will be saved in request object for view to use.
    UserId will also be saved as userId also if available.
    Decrypted or original request body will be convert into json object and saved as dictBody in request.
    :param need_login: Verification for post-login request
    :param need_decrypt: Process decryption of request body
    :return: view function
    """

    def decorate(view_func):
        def check(*args, **kwargs):
            request = args[0]
            request.need_login = need_login
            request.need_decrypt = need_decrypt
            body = request.body
            if need_decrypt:
                body = decrypt(body, True)
            try:
                body = json.loads(body)
                request.dictBody = body
            except Exception, e:
                log.error(e.message)
                return ResponseObject(1000, u'无效的请求').toJSONHttpResponse()
            # Need_decrypt is True means request is coming from Mobile
            # -> userId is part of json body
            # If it's False, means coming from H5 or web application
            # -> userId is store in session
            if need_decrypt:
                userId = body.get('userId', None)
            else:
                userId = request.session.get('userId', None)
            request.userId = userId
            if need_login:
                # Validate the userId
                if not userId:
                    return ResponseObject(1001, u'未登录').toJSONHttpResponse()
                if User.objects.filter(userId=userId, status__key='ACTIVE').count() == 0:
                    return ResponseObject(1002, u'无效用户或账户异常').toJSONHttpResponse()
            # Continue view process
            try:
                return view_func(*args, **kwargs)
            except Exception, e:
                log.error(e.message)
                return ResponseObject(2000, '%s' % e.message).toJSONHttpResponse()

        return check

    return decorate


# For Web app, if it's on application server
def requireWebProcess(need_login=True):
    """
    Decoration for preprocess of each request.

    Parameter need_login, need_decrypt will be saved in request object for view to use.
    UserId will also be saved as userId also if available.
    Decrypted or original request body will be convert into json object and saved as dictBody in request.
    :param need_login: Verification for post-login request
    :param need_decrypt: Process decryption of request body
    :return: view function
    """

    def decorate(view_func):
        def check(*args, **kwargs):
            request = args[0]
            request.need_login = need_login
            userId = request.session.get('userId', None)
            request.userId = userId
            if need_login and (not userId or User.objects.filter(userId=userId, status__key='ACTIVE').count() == 0):
                # Validate the userId
                return HttpResponseRedirect('login')
            # Continue view process, save request navigation path
            navPath = request.session.get('navPath', [])
            if len(navPath) == 0 or navPath[-1] != view_func.func_name:
                navPath.append(view_func.func_name)
            request.session['navPath'] = navPath
            try:
                return view_func(*args, **kwargs)
            except Exception, e:
                log.error(e.message)
                return THR(request, 'xiaoye/error.html', {'error': e.message})

        return check

    return decorate


def parseFilter(filter, context):
    if type(filter) == str or type(filter) == unicode:
        v = filter
    else:
        v = filter.resolve(context)
        if v == '':
            v = filter
    return v


def getPhrase(request, appid, phraseid, default=None):
    """The function return the phrase text against language in session"""
    lan = request.session.get('lan', 'cn')
    p = SitePhrase.objects.filter(app__appId=appid, phraseId=phraseid, phraseLan__key=lan)
    if p and p[0]:
        if p[0].content:
            htmlContent = p[0].content
        else:
            htmlContent = p[0].bigContent
    else:
        if default:
            htmlContent = default
        else:
            htmlContent = "[%s %s %s]" % (appid, phraseid, lan)
    return htmlContent


def sendRequest(url, headers, body):
    # ssl._create_default_https_context = ssl._create_unverified_context
    req = urllib2.Request(url)
    for k, v in headers.items():
        req.add_header(k, v)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
    try:
        response = opener.open(req, body)
        return (response.code, '', response.read())
    except urllib2.HTTPError, e:
        return (e.code, e.reason, e.read())
    except urllib2.URLError, e:
        return (None, e.reason, None)


def sendRequest2(url, headers, body):
    # ssl._create_default_https_context = ssl._create_unverified_context
    req = urllib2.Request(url)
    for k, v in headers.items():
        req.add_header(k, v)
    # Get method by urllib
    try:
        response = urllib2.urlopen(req, body)
        return (response.code, None, response.read())
    except urllib2.HTTPError, e:
        return (e.code, e.reason, e.read())
    except urllib2.URLError, e:
        return (None, e.reason, None)


def getWXToken(appId, secret):
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
    url = url % (appId, secret)
    headers = {}
    headers['Content-Type'] = 'application/json'
    body = ""
    (code, reason, result) = sendRequest(url, headers, body)
    # Fake result
    # result = """
    # {"access_token":"ZTNaZsZqb43FMLBLLnZGhPGA22E4uioreRkzvFIi44NaTvbdIaWvMFP9H0DjfpwkGnK43GMou9vJfxJX-W41fHGG_On0neQYdZMQDbkAzDXH73fkY9LJchAW38l-wQoECIXeACATZO","expires_in":7200}
    # """
    return result


def getSystemConfigByKey(key, property1=None, property2=None):
    filter = {}
    filter['key'] = key
    if property1:
        filter['property1'] = property1
    if property2:
        filter['property2'] = property2
    try:
        sc = SystemConfiguration.objects.get(**filter)
        result = {}
        result['property1'] = sc.property1
        result['property2'] = sc.property2
        result['value1'] = sc.value1
        result['value2'] = sc.value2
        result['text1'] = sc.text1
        result['text2'] = sc.text2
        return result
    except Exception, e:
        return None


def setSystemConfigByKey(key, configDict):
    try:
        configDict['key'] = key
        SystemConfiguration.objects.update_or_create(**configDict)
        return True
    except Exception, e:
        return False


# For Weixin backend
class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''

    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})


class WebChat:
    token = ''
    debug = False

    def __init__(self, token, debug=False):
        self.token = token
        self.debug = debug

    def isValid(self, request):
        return request.GET.get('echostr', None) != None

    def validateSignature(self, request):
        signature = request.GET.get('signature', None)
        log.info('signature %s' % signature)
        timestamp = request.GET.get('timestamp', None)
        log.info('timestamp %s' % timestamp)
        nonce = request.GET.get('nonce', None)
        log.info('nonce %s' % nonce)
        signatureArray = [self.token, timestamp, nonce]
        signatureArray.sort()
        log.info('signatureArray sorted %s' % signatureArray)
        tempStr = ''.join(signatureArray)
        log.info('signStr %s' % tempStr)
        sha1TempStr = hashlib.sha1(tempStr).hexdigest()
        log.info('sha1Str %s' % sha1TempStr)
        return sha1TempStr == signature

    def returnTextResponse(self, toUserName, fromUserName, content, funcFlag=0):
        response = """
        <xml>
  <ToUserName><![CDATA[%(toUserName)s]]></ToUserName>
  <FromUserName><![CDATA[%(fromUserName)s]]></FromUserName>
  <CreateTime>%(createTime)s</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[%(content)s]]></Content>
  <FuncFlag>%(funcFlag)s<FuncFlag>
</xml>""" % {
            "toUserName": toUserName,
            "fromUserName": fromUserName,
            "createTime": datetime.datetime.now(),
            "content": content,
            "funcFlag": funcFlag
        }
        return response

    def returnSingleNewsItem(self, title, description, picUrl, url):
        response = """
        <item>
  <Title><![CDATA[%s]]></Title>
  <Description><![CDATA[%s]]></Description>
  <PicUrl><![CDATA[%s]]></PicUrl>
  <Url><![CDATA[%s]]></Url>
</item>""" % (title, description, picUrl, url)
        return response

    def returnNewsResponse(self, toUserName, fromUserName, items, funcFlag=0):
        response = """
        <xml>
  <ToUserName><![CDATA[%(toUserName)s]]></ToUserName>
  <FromUserName><![CDATA[%(fromUserName)s]]></FromUserName>
  <CreateTime>%(createTime)s</CreateTime>
  <MsgType><![CDATA[news]]></MsgType>
  <ArticleCount>%(articleCount)s</ArticleCount>
  <Articles>
    %(articles)s
  </Articles>
  <FuncFlag>%(funcFlag)s<FuncFlag>
</xml>""" % {
            "toUserName": toUserName,
            "fromUserName": fromUserName,
            "createTime": datetime.datetime.now(),
            "articleCount": len(items),
            "articles": ''.join(items),
            "funcFlag": funcFlag
        }
        return response


class WebSite:
    apps = {}

    def handle(self, request):
        nav = {}
        if request.method == 'POST':
            # Get posted data : pageAction, pageParams, pageMode
            nav['pageApp'] = request.POST.get('pageApp', '')
            nav['pageAction'] = request.POST.get('pageAction', '')
            nav['pageParams'] = request.POST.get('pageParams', '')
            nav['pageMode'] = request.POST.get('pageMode', '')
        else:
            nav['pageApp'] = 'home'
        app = self.apps.get(nav['pageApp'], None)
        if app:
            return app.handle(request)
        return THR(request, 'xiaoye/index.html', {})


class Application:
    def handle(self, request):
        return THR(request, 'xiaoye/app1_1.html', {})


home = Application()

webSite = WebSite()
webSite.apps['home'] = home


class Crawler:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def dbcommit(self):
        pass

    def getentryid(self, table, field, value, createnew=True):
        pass

    def addtoindex(self, url, soup):
        print 'Indexing %s' % url

    def gettextonly(self, soup):
        return None

    def separatewords(self, text):
        return None

    def isindexed(self, url):
        return False

    def addlinkref(self, urlForm, urlTo, linkText):
        pass

    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                (code, reason, result) = sendRequest(page, {}, None)
                if code != 200:
                    print "Could not open %s" % page
                    continue
                print "%s %s %s" % (code, reason, result)
                soup = bs4.BeautifulSoup(result)
                self.addtoindex(page, soup)
                links = soup('a')
                # print links
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url = urlparse.urljoin(page, link['href'])
                        print 'urljoin %s' % url
                        if url.find("'") != -1:
                            continue
                        url = url.split('#')[0]
                        if url[0:4] == 'http' and not self.isindexed(url):
                            print url
                            newpages.add(url)
                        linkText = self.gettextonly(link)
                        self.addlinkref(page, url, linkText)
                    self.dbcommit()
                pages = newpages

    def createindextables(self):
        pass
