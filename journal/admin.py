from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from journal.models import Journal


@admin.register(Journal)
class JournalAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'number', 'year', 'get_articles', 'file_pdf', 'created_at', 'status', 'is_publish']