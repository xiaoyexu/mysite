from django.contrib import admin
from xiaoye.models import *


class UserStatusAdmin(admin.ModelAdmin):
    search_fields = ('key', 'description')
    list_display = ('key', 'description')


admin.site.register(UserStatus, UserStatusAdmin)


class UserAdmin(admin.ModelAdmin):
    search_fields = (
        'userId', 'loginName', 'loginCredential', 'status')
    list_display = (
        'userId', 'loginName', 'loginCredential', 'status')


admin.site.register(User, UserAdmin)


class RaspTemperatureAdmin(admin.ModelAdmin):
    search_fields = (
        'checkedAt', 'temperature', 'model')
    list_display = (
        'checkedAt', 'temperature', 'model')


admin.site.register(RaspTemperature, RaspTemperatureAdmin)


class WeixinUserAdmin(admin.ModelAdmin):
    search_fields = ('wxUnionid', 'wxOpenId', 'wxName')
    list_display = ('wxUnionid', 'wxOpenId', 'wxName')


admin.site.register(WeixinUser, WeixinUserAdmin)


class SystemConfigurationAdmin(admin.ModelAdmin):
    search_fields = ('key', 'property1', 'property2', 'value1', 'value2', 'text1', 'text2')
    list_display = ('key', 'property1', 'property2', 'value1', 'value2', 'text1', 'text2')


admin.site.register(SystemConfiguration, SystemConfigurationAdmin)


class WeixinMsgAdmin(admin.ModelAdmin):
    search_fields = ('fromUserName', 'createTime', 'msgType', 'content', 'msgId', 'createdAt')
    list_display = ('fromUserName', 'createTime', 'msgType', 'content', 'msgId', 'createdAt')


admin.site.register(WeixinMsg, WeixinMsgAdmin)
