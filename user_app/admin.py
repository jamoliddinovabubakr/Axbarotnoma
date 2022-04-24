from django.contrib import admin
from django.contrib.auth.models import Permission
from user_app.models import Role, Region, District, Gender, State, User, Notification, Menu

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'key']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'region']


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent_id', 'status', 'url', 'type_menu', 'icon']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'from_user_id', 'to_user_id', 'status', 'created_at']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'middle_name', 'birthday', 'gender', 'avatar', 'email',
                    'phone', 'passport', 'work_place', 'position', 'role', 'region', 'district']



