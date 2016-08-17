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
