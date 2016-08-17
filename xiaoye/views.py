from django.shortcuts import render
from xiaoye.common import *

def jsonResult(request):
    ro = ResponseObject(0, u'')
    return ro.toJSONHttpResponse()