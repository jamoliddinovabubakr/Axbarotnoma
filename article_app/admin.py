from django.contrib import admin
from article_app.models import Category, Article, Shartnoma, Authors, Page, Magazine, Post, BlankPage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'key', 'status']


@admin.register(Shartnoma)
class ShartnomaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'body', 'status']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'value']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'tag', 'desc', 'img', 'is_publish', 'created_at']
    prepopulated_fields = {'url': ('title', )}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'editor', 'analyst',
                    'file', 'state_edit', 'state_analysis', 'created_at', 'status', 'payed', 'is_publish']


@admin.register(Authors)
class AuthorsAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'middle_name', 'email', 'article', 'work_place', 'author_order']


@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ['id', 'number_magazine', 'year_magazine', 'get_articles', 'file_pdf', 'created_at', 'status']


@admin.register(BlankPage)
class BlankPageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'body', 'is_publish', 'created_at']