# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xiaoye', '0007_roomtemp'),
    ]

    operations = [
        migrations.CreateModel(
            name='HiddenNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hiddenKey', models.CharField(max_length=255, null=True, verbose_name='\u8282\u70b9\u4e3b\u952e', blank=True)),
            ],
            options={
                'verbose_name': '\u9690\u85cf\u8282\u70b9\u8868',
                'verbose_name_plural': '\u9690\u85cf\u8282\u70b9\u8868',
            },
        ),
        migrations.CreateModel(
            name='HiddenOutputMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.FloatField(default=1, verbose_name='\u6743\u91cd')),
                ('hiddenNode', models.ForeignKey(verbose_name='\u8282\u70b9', to='xiaoye.HiddenNode')),
            ],
            options={
                'verbose_name': '\u9690\u85cf\uff0d\u8f93\u51fa\u5173\u8054\u8868',
                'verbose_name_plural': '\u9690\u85cf\uff0d\u8f93\u51fa\u5173\u8054\u8868',
            },
        ),
        migrations.CreateModel(
            name='InputHiddenMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.FloatField(default=1, verbose_name='\u6743\u91cd')),
                ('hiddenNode', models.ForeignKey(verbose_name='\u8282\u70b9', to='xiaoye.HiddenNode')),
            ],
            options={
                'verbose_name': '\u8f93\u5165\uff0d\u9690\u85cf\u5173\u8054\u8868',
                'verbose_name_plural': '\u8f93\u5165\uff0d\u9690\u85cf\u5173\u8054\u8868',
            },
        ),
        migrations.CreateModel(
            name='InputValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=255, null=True, verbose_name='\u8f93\u5165\u503c', blank=True)),
                ('weight', models.FloatField(default=1, verbose_name='\u8f93\u5165\u7aef\u6743\u91cd')),
            ],
            options={
                'verbose_name': '\u8f93\u5165\u4fe1\u606f\u8868',
                'verbose_name_plural': '\u8f93\u5165\u4fe1\u606f\u8868',
            },
        ),
        migrations.CreateModel(
            name='OutputValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=255, null=True, verbose_name='\u8f93\u51fa\u503c', blank=True)),
            ],
            options={
                'verbose_name': '\u8f93\u51fa\u4fe1\u606f\u8868',
                'verbose_name_plural': '\u8f93\u51fa\u4fe1\u606f\u8868',
            },
        ),
        migrations.AddField(
            model_name='inputhiddenmapping',
            name='inputValue',
            field=models.ForeignKey(verbose_name='\u8f93\u5165', to='xiaoye.InputValue'),
        ),
        migrations.AddField(
            model_name='hiddenoutputmapping',
            name='outputValue',
            field=models.ForeignKey(verbose_name='\u8f93\u51fa', to='xiaoye.OutputValue'),
        ),
    ]
