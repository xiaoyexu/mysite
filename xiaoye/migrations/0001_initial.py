# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, verbose_name='\u7528\u6237ID')),
                ('loginName', models.CharField(max_length=50, null=True, verbose_name='\u767b\u5f55\u540d', blank=True)),
                ('loginCredential', models.CharField(max_length=50, null=True, verbose_name='\u5bc6\u7801', blank=True)),
                ('loginCredentialEncrypted', models.BooleanField(default=False, verbose_name='\u662f\u5426\u52a0\u5bc6')),
            ],
            options={
                'verbose_name': '\u79fb\u52a8\u7528\u6237\u8868',
                'verbose_name_plural': '\u79fb\u52a8\u7528\u6237\u8868',
            },
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('key', models.CharField(max_length=50, serialize=False, verbose_name='\u4e3b\u952e', primary_key=True)),
                ('description', models.CharField(max_length=255, null=True, verbose_name='\u63cf\u8ff0', blank=True)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u72b6\u6001\u5b9a\u4e49\u8868',
                'verbose_name_plural': '\u7528\u6237\u72b6\u6001\u5b9a\u4e49\u8868',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.ForeignKey(verbose_name='\u72b6\u6001', to='xiaoye.UserStatus'),
        ),
    ]
