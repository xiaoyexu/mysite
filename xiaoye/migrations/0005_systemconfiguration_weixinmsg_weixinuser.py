# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xiaoye', '0004_rasptemperature_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemConfiguration',
            fields=[
                ('key', models.CharField(max_length=50, serialize=False, verbose_name='\u4e3b\u952e', primary_key=True)),
                ('property1', models.CharField(max_length=50, null=True, verbose_name='\u5c5e\u60271', blank=True)),
                ('property2', models.CharField(max_length=50, null=True, verbose_name='\u5c5e\u60272', blank=True)),
                ('value1', models.CharField(max_length=255, null=True, verbose_name='\u503c1', blank=True)),
                ('value2', models.CharField(max_length=255, null=True, verbose_name='\u503c2', blank=True)),
                ('text1', models.TextField(null=True, verbose_name='\u6587\u672c1', blank=True)),
                ('text2', models.TextField(null=True, verbose_name='\u6587\u672c2', blank=True)),
            ],
            options={
                'verbose_name': '\u7cfb\u7edf\u914d\u7f6e\u8868',
                'verbose_name_plural': '\u7cfb\u7edf\u914d\u7f6e\u8868',
            },
        ),
        migrations.CreateModel(
            name='WeixinMsg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fromUserName', models.CharField(max_length=255, null=True, verbose_name='\u7528\u6237', blank=True)),
                ('createTime', models.CharField(max_length=255, null=True, verbose_name='\u65f6\u95f4', blank=True)),
                ('msgType', models.CharField(max_length=255, null=True, verbose_name='\u6d88\u606f\u7c7b\u578b', blank=True)),
                ('content', models.TextField(null=True, verbose_name='\u6d88\u606f\u6587\u672c', blank=True)),
                ('msgId', models.CharField(max_length=255, null=True, verbose_name='\u6d88\u606f\u53f7', blank=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u5fae\u4fe1\u516c\u4f17\u53f7\u6d88\u606f\u8868',
                'verbose_name_plural': '\u5fae\u4fe1\u516c\u4f17\u53f7\u6d88\u606f\u8868',
            },
        ),
        migrations.CreateModel(
            name='WeixinUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wxUnionid', models.CharField(max_length=255, null=True, verbose_name='\u5fae\u4fe1\u7528\u6237UnionId', blank=True)),
                ('wxOpenId', models.CharField(max_length=255, null=True, verbose_name='\u5fae\u4fe1\u7528\u6237OpenId', blank=True)),
                ('wxName', models.CharField(max_length=255, null=True, verbose_name='\u5fae\u4fe1\u7528\u6237\u540d\u79f0', blank=True)),
            ],
            options={
                'verbose_name': '\u5fae\u4fe1\u516c\u4f17\u53f7\u7528\u6237\u8868',
                'verbose_name_plural': '\u5fae\u4fe1\u516c\u4f17\u53f7\u7528\u6237\u8868',
            },
        ),
    ]
