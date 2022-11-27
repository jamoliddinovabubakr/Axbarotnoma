from django.contrib import admin
from django.contrib.auth.models import Permission
from import_export.admin import ImportExportActionModelAdmin
from modeltranslation.admin import TranslationAdmin

from user_app.models import *


@admin.register(Permission)
class PermissionAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'content_type', 'codename']


@admin.register(Region)
class RegionAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name']


@admin.register(Gender)
class GenderAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name']


@admin.register(Role)
class RoleAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name']


@admin.register(Menu)
class MenuAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'status',
                    'url', 'icon', 'menu_tr', 'get_roles']


@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'username', 'last_name', 'first_name', 'middle_name', 'birthday', 'gender', 'avatar', 'email',
                    'phone', 'pser', 'pnum', 'region', 'work', 'get_roles', 'created_at', 'updated_at']


@admin.register(Editor)
class EditorAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'user']


@admin.register(Reviewer)
class ReviewerAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'user', 'mfile', 'is_reviewer', 'created_at', 'updated_at']
    
    
@admin.register(StatusReview)
class StatusReviewerAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name']


@admin.register(ReviewerArticle)
class ReviewerArticleAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'article', 'reviewer', 'editor',
                    'status', 'comment', 'created_at']
