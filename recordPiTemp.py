# -*- coding: UTF-8 -*-
__author__ = 'xuxiaoye'

import os, django

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from xiaoye.models import *

rt = RaspTemperature()
rt.temperature = int(open("/sys/class/thermal/thermal_zone0/temp", "r").read()) / 1000.0
rt.save()
