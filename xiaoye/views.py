# -*- coding: UTF-8 -*-
from django.shortcuts import render
from xiaoye.common import *


@requireProcess(need_login=True)
def jsonResult(request):
    ro = ResponseObject(0, u'')
    return ro.toJSONHttpResponse()


def index(request):
    return THR(request, 'xiaoye/index.html', {})
