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
            key = 'abcdefghijklmnopqrstuvwx'
            # 3DES Initial vector
            iv = '12345678'
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
            if need_login:
                # Validate the userId
                if not userId or User.objects.filter(userId=userId, status__key='ACTIVE').count() == 0:
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
