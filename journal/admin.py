from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from journal.models import SplitPdf, Journal

admin.site.register(SplitPdf)


@admin.register(Journal)
class JournalAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'journal_number', 'journal_year', 'get_articles', 'file_pdf', 'created_at', 'status']