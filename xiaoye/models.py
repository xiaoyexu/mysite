# -*- coding: UTF-8 -*-
from django.db import models
import uuid


class UserStatus(models.Model):
    key = models.CharField(max_length=50, primary_key=True, verbose_name=u"主键")
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"描述")

    def __unicode__(self):
        return "%s %s" % (self.key, self.description)

    class Meta:
        verbose_name = u"用户状态定义表"
        verbose_name_plural = u"用户状态定义表"


class User(models.Model):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=u"用户ID")
    loginName = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"登录名")
    loginCredential = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"密码")
    loginCredentialEncrypted = models.BooleanField(default=False, verbose_name=u"是否加密")
    status = models.ForeignKey('UserStatus', verbose_name=u"状态")

    def __unicode__(self):
        return "%s %s" % (self.userId, self.loginName)

    class Meta:
        verbose_name = u"移动用户表"
        verbose_name_plural = u"移动用户表"


# This table defines site language, e.g.
# en English
# cn Chinese
class SiteLanguage(models.Model):
    key = models.CharField(max_length=5, verbose_name=u"主键")
    description = models.CharField(max_length=50, verbose_name=u"语言描述")

    def __unicode__(self):
        return "%s(%s)" % (self.key, self.description)

    class Meta:
        verbose_name = u"网站语言"
        verbose_name_plural = u"网站语言"


# This table defines site application name for phrase, e.g.
# default
# login
class SiteAppType(models.Model):
    appId = models.CharField(max_length=20, primary_key=True, verbose_name=u"应用主键")
    description = models.CharField(max_length=50, verbose_name=u"描述")

    def __unicode__(self):
        return "%s(%s)" % (self.appId, self.description)

    class Meta:
        verbose_name = u"网站应用定义表"
        verbose_name_plural = u"网站应用定义表"


# This table defines phrase in site
class SitePhrase(models.Model):
    phraseId = models.CharField(max_length=20, verbose_name=u"短语主键")
    app = models.ForeignKey('SiteAppType', verbose_name=u"应用")
    phraseLan = models.ForeignKey('SiteLanguage', verbose_name=u"语言")
    content = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"内容")
    bigContent = models.TextField(null=True, blank=True, verbose_name=u"大文本内容")

    class Meta:
        unique_together = ("phraseId", "app", "phraseLan")
        verbose_name = u"网站短语国际化表"
        verbose_name_plural = u"网站短语国际化表"

    def __unicode__(self):
        return "%s %s %s %s" % (self.phraseId, self.app.description, self.phraseLan.description, self.content)
