from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'key', 'status']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'abstract', 'keywords', 'references', 'author', 'editor', 'analyst',
                    'file', 'state_edit', 'state_analysis', 'created_at', 'status', 'payed', 'url']
