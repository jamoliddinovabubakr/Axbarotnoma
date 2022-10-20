from django.contrib import admin
from article_app.models import *
from import_export.admin import ImportExportActionModelAdmin


@admin.register(Category)
class CategoryAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'status']


@admin.register(MyResendArticle)
class MyResendArticleAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'article', 'file_word', 'message', 'state', 'created_at']


@admin.register(Post)
class PostAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'title', 'tag', 'desc', 'img', 'is_publish', 'created_at']
    prepopulated_fields = {'url': ('title', )}


@admin.register(Article)
class ArticleAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'get_categories', 'title', 'author',
                    'file', 'file_pdf', 'state','created_at', 'is_publish']


@admin.register(Authors)
class AuthorsAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'article', 'first_name', 'last_name', 'middle_name', 'email', 'work_place', 'author_order']


@admin.register(Journal)
class MagazineAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'number_magazine', 'year_magazine', 'get_articles', 'file_pdf', 'created_at', 'status']


@admin.register(BlankPage)
class BlankPageAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'title', 'body', 'is_publish', 'created_at']