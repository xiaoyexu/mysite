# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xiaoye', '0003_accesslog_rasptemperature'),
    ]

    operations = [
        migrations.AddField(
            model_name='rasptemperature',
            name='model',
            field=models.CharField(max_length=10, null=True, verbose_name='\u578b\u53f7', blank=True),
        ),
    ]
