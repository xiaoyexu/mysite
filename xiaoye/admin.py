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


class RoomTempAdmin(admin.ModelAdmin):
    search_fields = (
        'checkedAt', 'temperature', 'humidity')
    list_display = (
        'checkedAt', 'temperature', 'humidity')


admin.site.register(RoomTemp, RoomTempAdmin)


class WeixinUserAdmin(admin.ModelAdmin):
    search_fields = ('wxUnionid', 'wxOpenId', 'wxName')
    list_display = ('wxUnionid', 'wxOpenId', 'wxName')


admin.site.register(WeixinUser, WeixinUserAdmin)


class SystemConfigurationAdmin(admin.ModelAdmin):
    search_fields = ('key', 'property1', 'property2', 'value1', 'value2', 'text1', 'text2')
    list_display = ('key', 'property1', 'property2', 'value1', 'value2', 'text1', 'text2')


admin.site.register(SystemConfiguration, SystemConfigurationAdmin)


class WeixinMsgAdmin(admin.ModelAdmin):
    search_fields = ('createTime', 'msgType', 'content', 'msgId', 'event', 'eventKey', 'createdAt')
    list_display = ('fromUser', 'createTime', 'msgType', 'content', 'msgId', 'event', 'eventKey', 'createdAt')


admin.site.register(WeixinMsg, WeixinMsgAdmin)


class InputValueAdmin(admin.ModelAdmin):
    list_display = ('value', 'weight')


admin.site.register(InputValue, InputValueAdmin)


class HiddenNodeAdmin(admin.ModelAdmin):
    list_display = ('hiddenKey',)


admin.site.register(HiddenNode, HiddenNodeAdmin)


class OutputValueAdmin(admin.ModelAdmin):
    list_display = ('value',)


admin.site.register(OutputValue, OutputValueAdmin)


class InputHiddenMappingAdmin(admin.ModelAdmin):
    list_display = ('inputValue', 'hiddenNode', 'weight')


admin.site.register(InputHiddenMapping, InputHiddenMappingAdmin)


class HiddenOutputMappingAdmin(admin.ModelAdmin):
    list_display = ('hiddenNode', 'outputValue', 'weight')


admin.site.register(HiddenOutputMapping, HiddenOutputMappingAdmin)
