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

# SiteAppType
records = [
    ['default', u'Global default module']
]
for record in records:
    r = {}
    r['appId'] = record[0]
    r['description'] = record[1]
    SiteAppType.objects.update_or_create(**r)

# SiteLanguage
records = [
    ['cn', u'中文'],
    ['en', u'English']
]
for record in records:
    r = {}
    r['key'] = record[0]
    r['description'] = record[1]
    SiteLanguage.objects.update_or_create(**r)


# SitePhrase
phrases = [
    ['home', 'default', 'cn', u'首页'],
    ['home', 'default', 'en', u'Home']
]

for phrase in phrases:
    p = {}
    p['phraseId'] = phrase[0]
    p['app'] = SiteAppType.objects.get(appId=phrase[1])
    p['phraseLan'] = SiteLanguage.objects.get(key=phrase[2])
    p['content'] = phrase[3]
    SitePhrase.objects.update_or_create(**p)
