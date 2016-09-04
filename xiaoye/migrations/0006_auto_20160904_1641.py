# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xiaoye', '0005_systemconfiguration_weixinmsg_weixinuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weixinmsg',
            name='fromUserName',
        ),
        migrations.AddField(
            model_name='weixinmsg',
            name='event',
            field=models.CharField(max_length=255, null=True, verbose_name='\u4e8b\u4ef6\u7c7b\u578b', blank=True),
        ),
        migrations.AddField(
            model_name='weixinmsg',
            name='eventKey',
            field=models.CharField(max_length=255, null=True, verbose_name='\u4e8b\u4ef6', blank=True),
        ),
        migrations.AddField(
            model_name='weixinmsg',
            name='fromUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u7528\u6237', blank=True, to='xiaoye.WeixinUser', null=True),
        ),
    ]
