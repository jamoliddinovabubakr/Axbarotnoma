from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from journal.models import SplitPdf, Journal, BlankPage, Post

admin.site.register(SplitPdf)


@admin.register(Journal)
class JournalAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'journal_number', 'journal_year', 'get_articles', 'file_pdf', 'created_at', 'status']


@admin.register(BlankPage)
class BlankPageAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'title', 'body', 'is_publish', 'created_at']


@admin.register(Post)
class PostAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'title', 'tag', 'desc', 'img', 'is_publish', 'created_at']
    prepopulated_fields = {'url': ('title',)}
