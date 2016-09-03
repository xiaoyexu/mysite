# My Django Site
Used to figure out basic essentials of setting up a django website.

# Models
## User
A simple User table to store user data such as username, password, status etc.

## UserStatus
A Foreign key in user table refer to the status code.

## SiteLanguage
Store basic site language info, simple as cn for Chinese or en for English

## SiteAppType
Category of phrase/text type, grouped by application

## SitePhrase
Phrase table for any text displayed on web site. E.g

PhraseId | SiteAppType | SiteLanguage | Text
------- | ------- | ------- | -------
home | default | en | Home
home | default | cn | 首页

Related tag: [PhraseTag](#phraseTag)

## RaspTemperature
Table to store raspberry pi CPU temperature.
A cron job is set to record temperature every minute.

```
# -*- coding: UTF-8 -*-
__author__ = 'xuxiaoye'

import os, django

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from xiaoye.models import *

rt = RaspTemperature()
rt.temperature = int(open("/sys/class/thermal/thermal_zone0/temp", "r").read()) / 1000.0
rt.save()
```

# Views
## index
Default entry

## back
Handle any back action

## logoff
Handle logoff action




# Tag
## <span id="phraseTag">PhraseTag</span>
Read phrase from database table

```
{% PhraseTag default home %}
```


