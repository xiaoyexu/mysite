# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xiaoye', '0006_auto_20160904_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomTemp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('checkedAt', models.DateTimeField(auto_now_add=True, verbose_name='\u65f6\u95f4')),
                ('temperature', models.FloatField(default=0, null=True, verbose_name='\u6e29\u5ea6', blank=True)),
                ('humidity', models.FloatField(default=0, null=True, verbose_name='\u6e7f\u5ea6', blank=True)),
            ],
            options={
                'verbose_name': '\u6e29\u6e7f\u5ea6\u8868',
                'verbose_name_plural': '\u6e29\u6e7f\u5ea6\u8868',
            },
        ),
    ]
