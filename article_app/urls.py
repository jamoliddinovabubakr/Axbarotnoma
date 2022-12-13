from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    path('', main_page, name='main_page'),
    path('contact/', TemplateView.as_view(template_name="article_app/contact.html"), name='contact'),
    path('aboutdtm/', TemplateView.as_view(template_name="article_app/blank_page/about_dtm.html"), name='aboutdtm'),
    path('editor_board/', TemplateView.as_view(template_name="article_app/blank_page/editor_board.html"),
         name='editor_board'),

    # path('post/<slug:slug>/', post_detail, name='post_detail'),

    path('article/create/', create_article, name='create_article'),
    path('article/view/<int:pk>/', article_view, name='article_view'),
    path('article/edit/<int:pk>/', update_article, name='update_article'),
    path('article/delete/<int:pk>/', delete_article, name='delete_article'),
    path('article/file/create/<int:pk>/', create_article_file, name='create_article_file'),

    path('authors/<int:pk>/', get_article_authors, name='get_article_authors'),
    path('author/add/<int:pk>/', add_author, name='add_author'),
    path('author/edit/<int:pk>/', edit_author, name='edit_author'),
    path('author/delete/<int:pk>/', delete_author, name='delete_author'),

    path('send_message/<int:pk>/<int:user_id>', send_message, name='send_message'),

    path('sections/', list_sections, name='sections'),
    path('article_types/', article_type_list, name='article_types'),
    path('article_stages/', article_stages_list, name='article_stages'),
    path('article_status/', article_status_list, name='article_status'),
    path('notification_status/', notification_status_list, name='notification_status'),
    path('category/delete/<int:pk>/', delete_category, name='delete_category'),

]
