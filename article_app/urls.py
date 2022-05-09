from django.urls import path, include, re_path
from .views import main_page, add_article

urlpatterns = [
    path('', main_page, name='main_page'),
    path('add_article/', add_article, name='add_article'),
]