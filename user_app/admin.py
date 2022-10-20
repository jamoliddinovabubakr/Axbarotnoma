from django.contrib import admin
from django.contrib.auth.models import Permission
from import_export.admin import ImportExportActionModelAdmin

from user_app.models import *


@admin.register(Permission)
class PermissionAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name']


@admin.register(Role)
class RoleAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'status']


@admin.register(State)
class StateAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'status']


@admin.register(Region)
class RegionAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'key']


# @admin.register(Gender)
# class GenderAdmin(ImportExportActionModelAdmin):
#     list_display = ['id', 'name', 'status']


@admin.register(Menu)
class MenuAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'parent_id', 'status',
                    'url', 'type_menu', 'icon', 'menu_tr', 'get_roles']


@admin.register(Notification)
class NotificationAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'article', 'title',
                    'description', 'status', 'created_at', 'my_resend']


@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'middle_name', 'birthday', 'avatar', 'email',
                    'phone', 'passport', 'role', 'region']
