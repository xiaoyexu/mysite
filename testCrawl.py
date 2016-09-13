# -*- coding: UTF-8 -*-
__author__ = 'xuxiaoye'

import os, django
import re

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from xiaoye.models import *
from xiaoye.common import *

url = 'http://tianqi.moji.com/weather/china/shanghai/shanghai'
(code, reason, result) = sendRequest(url, {}, None)
if code != 200:
    print "Could not open %s" % url
    exit(0)

# print "%s %s %s" % (code, reason, result)
soup = bs4.BeautifulSoup(result)
dr = re.compile(r'<[^>]+>', re.S)
dd = dr.sub('', str(soup('em')[2]))
temp = dd
dd = dr.sub('', str(soup('span')[2]))
hum =  re.match('[^1-9]*(\d*)?[^1-9]*', dd).groups()[0]
print '->%s %s' % (temp, hum)