# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xiaoye', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteAppType',
            fields=[
                ('appId', models.CharField(max_length=20, serialize=False, verbose_name='\u5e94\u7528\u4e3b\u952e', primary_key=True)),
                ('description', models.CharField(max_length=50, verbose_name='\u63cf\u8ff0')),
            ],
            options={
                'verbose_name': '\u7f51\u7ad9\u5e94\u7528\u5b9a\u4e49\u8868',
                'verbose_name_plural': '\u7f51\u7ad9\u5e94\u7528\u5b9a\u4e49\u8868',
            },
        ),
        migrations.CreateModel(
            name='SiteLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=5, verbose_name='\u4e3b\u952e')),
                ('description', models.CharField(max_length=50, verbose_name='\u8bed\u8a00\u63cf\u8ff0')),
            ],
            options={
                'verbose_name': '\u7f51\u7ad9\u8bed\u8a00',
                'verbose_name_plural': '\u7f51\u7ad9\u8bed\u8a00',
            },
        ),
        migrations.CreateModel(
            name='SitePhrase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phraseId', models.CharField(max_length=20, verbose_name='\u77ed\u8bed\u4e3b\u952e')),
                ('content', models.CharField(max_length=255, null=True, verbose_name='\u5185\u5bb9', blank=True)),
                ('bigContent', models.TextField(null=True, verbose_name='\u5927\u6587\u672c\u5185\u5bb9', blank=True)),
                ('app', models.ForeignKey(verbose_name='\u5e94\u7528', to='xiaoye.SiteAppType')),
                ('phraseLan', models.ForeignKey(verbose_name='\u8bed\u8a00', to='xiaoye.SiteLanguage')),
            ],
            options={
                'verbose_name': '\u7f51\u7ad9\u77ed\u8bed\u56fd\u9645\u5316\u8868',
                'verbose_name_plural': '\u7f51\u7ad9\u77ed\u8bed\u56fd\u9645\u5316\u8868',
            },
        ),
        migrations.AlterUniqueTogether(
            name='sitephrase',
            unique_together=set([('phraseId', 'app', 'phraseLan')]),
        ),
    ]
