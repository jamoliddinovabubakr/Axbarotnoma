from django.contrib import admin
from article_app.models import *
from import_export.admin import ImportExportActionModelAdmin


@admin.register(Section)
class SectionAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name']


@admin.register(Stage)
class StageAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name']


@admin.register(ArticleStatus)
class ArticleStatusAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'stage']


@admin.register(Article)
class ArticleAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'section', 'get_article_authors', 'file', 'title', 'abstract', 'keywords', 'references', 'article_status',
                    'is_publish', 'created_at', 'updated_at']


@admin.register(ArticleFile)
class ArticleFileAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'article', 'file', 'file_name',
                    'file_size', 'file_type', 'file_status', 'created_at']


@admin.register(Submission)
class SubmissionAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'article', 'author', 'article_status', 'created_at']


@admin.register(StatusReviewer)
class StatusReviewerAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'created_at']


@admin.register(ReviewerArticle)
class ReviewerArticleAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'article', 'reviewer', 'editor',
                    'status', 'comment', 'created_at']


@admin.register(NotificationStatus)
class NotificationStatusAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name']


@admin.register(Notification)
class NotificationAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'article', 'from_user', 'to_user', 'message', 'notification_status',
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
