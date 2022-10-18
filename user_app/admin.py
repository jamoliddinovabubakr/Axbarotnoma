from django.contrib import admin
from django.contrib.auth.models import Permission
from user_app.models import *


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'key']


# @admin.register(Gender)
# class GenderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'status']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent_id', 'status',
                    'url', 'type_menu', 'icon', 'menu_tr', 'get_roles']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'title',
                    'description', 'status', 'created_at', 'my_resend']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'middle_name', 'birthday', 'avatar', 'email',
                    'phone', 'passport', 'role', 'region']
