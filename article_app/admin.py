from django.contrib import admin
from article_app.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']


@admin.register(MyResendArticle)
class MyResendArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'file_word', 'message', 'state', 'created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'tag', 'desc', 'img', 'is_publish', 'created_at']
    prepopulated_fields = {'url': ('title', )}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'author',
                    'file', 'file_pdf', 'state','created_at', 'is_publish']


@admin.register(Authors)
class AuthorsAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'first_name', 'last_name', 'middle_name', 'email', 'work_place', 'author_order']


@admin.register(Journal)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ['id', 'number_magazine', 'year_magazine', 'get_articles', 'file_pdf', 'created_at', 'status']


@admin.register(BlankPage)
class BlankPageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'body', 'is_publish', 'created_at']