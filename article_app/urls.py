from django.urls import path, include, re_path
from .views import main_page, my_articles, create_article, update_my_article

urlpatterns = [
    path('', main_page, name='main_page'),
    path('my_articles/', my_articles, name='my_articles'),
    path('create_article/', create_article, name='create_article'),
    path('update_my_article/<int:pk>/', update_my_article, name='update_my_article'),
]