from django.contrib import admin
from article_app.models import *
from import_export.admin import ImportExportActionModelAdmin
from modeltranslation.admin import TranslationAdmin


@admin.register(Section)
class SectionAdmin(ImportExportActionModelAdmin, TranslationAdmin):
    list_display = ['id', 'name']


@admin.register(Stage)
class StageAdmin(ImportExportActionModelAdmin, TranslationAdmin):
    list_display = ['id', 'name']


@admin.register(ArticleStatus)
class ArticleStatusAdmin(ImportExportActionModelAdmin, TranslationAdmin):
    list_display = ['id', 'name', 'stage_id']


@admin.register(Article)
class ArticleAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'section_id', 'title', 'created_at',
                    'updated_at']


@admin.register(ArticleFile)
class ArticleFileAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'article_id', 'file', 'file_name',
                    'file_size', 'file_type', 'created_at', 'updated_at']


@admin.register(Submission)
class SubmissionAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'article_id', 'author_id', 'editor_id', 'file_id', 'article_status_id', 'created_at']


@admin.register(Review)
class ReviewAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'submission_id', 'reviewer_id', 'editor_id',
                    'file_id', 'comment', 'created_at']


@admin.register(NotificationStatus)
class NotificationStatusAdmin(ImportExportActionModelAdmin, TranslationAdmin):
    list_display = ['id', 'name']


@admin.register(Notification)
class NotificationAdmin(ImportExportActionModelAdmin, TranslationAdmin):
    list_display = ['id', 'submission_id', 'from_user_id', 'to_user_id', 'message', 'notification_status_id',
                    'created_at']


@admin.register(Post)
class PostAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'title', 'tag', 'desc', 'img', 'is_publish', 'created_at']
    prepopulated_fields = {'url': ('title',)}


@admin.register(Journal)
class JournalAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'journal_number', 'journal_year', 'get_articles', 'file_pdf', 'created_at', 'status']


@admin.register(BlankPage)
class BlankPageAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'title', 'body', 'is_publish', 'created_at']
