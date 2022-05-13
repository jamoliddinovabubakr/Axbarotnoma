from django.contrib import admin
from article_app.models import Category, Article, Shartnoma


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'key', 'status']


@admin.register(Shartnoma)
class ShartnomaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'body', 'status']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'editor', 'analyst',
                    'file', 'state_edit', 'state_analysis', 'created_at', 'status', 'payed']
