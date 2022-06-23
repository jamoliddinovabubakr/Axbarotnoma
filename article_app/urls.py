from django.urls import path, include, re_path
from .views import main_page, my_articles, create_article, update_my_article, add_author, edit_author, delete_author, \
    delete_myarticle, get_category, edit_category, delete_category, create_category

urlpatterns = [
    path('', main_page, name='main_page'),
    path('articles/', my_articles, name='my_articles'),
    path('article/create', create_article, name='create_article'),
    path('article/edit/<int:pk>/', update_my_article, name='update_my_article'),
    path('article/delete/<int:pk>/', delete_myarticle, name='delete_myarticle'),

    path('author/<int:pk>/', add_author, name='add_author'),
    path('author/edit/<int:pk>/', edit_author, name='edit_author'),
    path('author/delete/<int:pk>/', delete_author, name='delete_author'),

    path('categories/', get_category, name='get_category'),
    path('category/create/', create_category, name='create_category'),
    path('category/edit/<int:pk>/', edit_category, name='edit_category'),
    path('category/delete/<int:pk>/', delete_category, name='delete_category'),
]
