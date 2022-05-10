from django.contrib import admin
from article_app.models import Category, Article, Shartnoma, Author


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'key', 'status']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'article_id', 'last_name', 'middle_name', 'first_name', 'email', 'work_place', 'oreder']


@admin.register(Shartnoma)
class ShartnomaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'body', 'status']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'abstract', 'keywords', 'references', 'author', 'editor', 'analyst',
                    'file', 'state_edit', 'state_analysis', 'created_at', 'status', 'payed', 'url']
