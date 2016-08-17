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
