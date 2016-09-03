# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xiaoye', '0002_auto_20160818_0831'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accessAt', models.DateTimeField(auto_now_add=True, verbose_name='\u65f6\u95f4')),
                ('view', models.CharField(max_length=255, null=True, verbose_name='\u9875\u9762', blank=True)),
            ],
            options={
                'verbose_name': '\u8bbf\u95ee\u65e5\u5fd7',
                'verbose_name_plural': '\u8bbf\u95ee\u65e5\u5fd7',
            },
        ),
        migrations.CreateModel(
            name='RaspTemperature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('checkedAt', models.DateTimeField(auto_now_add=True, verbose_name='\u65f6\u95f4')),
                ('temperature', models.FloatField(default=0, null=True, verbose_name='\u6e29\u5ea6', blank=True)),
            ],
            options={
                'verbose_name': '\u6811\u8393\u6d3e3\u6e29\u5ea6\u8868',
                'verbose_name_plural': '\u6811\u8393\u6d3e3\u6e29\u5ea6\u8868',
            },
        ),
    ]
