# -*- coding: UTF-8 -*-
__author__ = 'xuxiaoye'

import os, django

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from xiaoye.models import *

# UserStatus
records = [
    ['ACTIVE', u'激活'],
    ['LOCK', u'已锁']
]
for record in records:
    r = {}
    r['key'] = record[0]
    r['description'] = record[1]
    UserStatus.objects.update_or_create(**r)