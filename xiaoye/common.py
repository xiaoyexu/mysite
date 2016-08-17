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
        return HttpResponse(json.dumps(self.getJSONDict()))

    def getJSONDict(self):
        return {'code': self.code, 'desc': self.desc, 'data': self.data}


def THR(request, template, context):
    """Return HttpResponse object with template and context"""
    template = loader.get_template(template)
    ctx = RequestContext(request, context)
    return HttpResponse(template.render(ctx))
