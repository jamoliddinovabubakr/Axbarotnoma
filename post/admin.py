from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from post.models import BlankPage, Post


@admin.register(BlankPage)
class BlankPageAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'title', 'body', 'is_publish', 'created_at']


@admin.register(Post)
class PostAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'title', 'tag', 'desc', 'img', 'is_publish', 'created_at']
    prepopulated_fields = {'url': ('title',)}
