from django.urls import path, include, re_path
from .views import main_page, my_articles, create_article, update_my_article, add_author, edit_author, delete_author, \
    delete_myarticle, get_category, edit_category, delete_category, create_category, create_magazine, get_magazines, edit_magazine, post_detail

urlpatterns = [
    path('', main_page, name='main_page'),
    path('<slug:slug>/', post_detail, name='post_detail'),


    path('articles/', my_articles, name='my_articles'),
    path('article/create', create_article, name='create_article'),
    path('article/edit/<int:pk>/', update_my_article, name='update_my_article'),
    path('article/delete/<int:pk>/', delete_myarticle, name='delete_myarticle'),

    path('author/<int:pk>/', add_author, name='add_author'),
    path('author/edit/<int:pk>/', edit_author, name='edit_author'),
    path('author/delete/<int:pk>/', delete_author, name='delete_author'),

    path('magazines/', get_magazines, name='get_magazines'),
    path('magazine/create', create_magazine, name='create_magazine'),
    path('magazine/edit/<int:pk>', edit_magazine, name='edit_magazine'),

    path('categories/', get_category, name='get_category'),
    path('category/create/', create_category, name='create_category'),
    path('category/edit/<int:pk>/', edit_category, name='edit_category'),
    path('category/delete/<int:pk>/', delete_category, name='delete_category'),

]
