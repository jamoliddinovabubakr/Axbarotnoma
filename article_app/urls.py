from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from .views import *


urlpatterns = [
    path('', main_page, name='main_page'),
    path('about_journal/', about_journal, name='about_journal'),
    path('talabnoma/', talabnoma, name='talabnoma'),
    path('all_magazines/', all_magazine_son, name='all_magazine_son'),
    path('contact/', TemplateView.as_view(template_name="article_app/contact.html"), name='contact'),
    path('aboutdtm/', TemplateView.as_view(template_name="article_app/blank_page/about_dtm.html"), name='aboutdtm'),
    path('editor_board/', TemplateView.as_view(template_name="article_app/blank_page/editor_board.html"),
         name='editor_board'),

    path('post/<slug:slug>/', post_detail, name='post_detail'),

    path('articles/', my_articles, name='my_articles'),

    path('article/create/', create_article, name='create_article'),
    path('article/view/<int:pk>/', article_view, name='article_view'),
    path('article/edit/<int:pk>/', update_article, name='update_article'),
    path('article/delete/<int:pk>/', delete_article, name='delete_article'),
    path('article/file/create/<int:pk>/', create_article_file, name='create_article_file'),

    path('search/author/', search_author, name='search_author'),
    path('authors/<int:pk>', get_article_authors, name='get_article_authors'),
    path('add_author/<int:pk>', add_author, name='add_author'),
    path('author/edit/<int:pk>/', edit_author, name='edit_author'),
    path('author/delete/<int:pk>/', delete_author, name='delete_author'),

    path('magazines/', get_magazines, name='get_magazines'),
    path('magazine/create', create_magazine, name='create_magazine'),
    path('magazine/view/<int:pk>/', magazine_detail, name='view_magazine'),
    path('magazine/edit/<int:pk>', edit_magazine, name='edit_magazine'),

    path('categories/', get_category, name='get_category'),
    # path('category/create/', create_category, name='create_category'),
    path('category/edit/<int:pk>/', edit_category, name='edit_category'),
    path('category/delete/<int:pk>/', delete_category, name='delete_category'),

]
