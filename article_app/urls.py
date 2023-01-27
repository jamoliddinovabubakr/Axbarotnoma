from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('', main_page, name='main_page'),
    path('contact/', contact, name='contact'),
    path('render_pdf/', render_pdf, name="render_pdf"),
    path('about_journal/', about_journal, name='about_journal'),
    path('editor_board/', editor_board, name='editor_board'),
    path('guide_for_authors/', guide_for_authors, name='guide_for_authors'),

    path('article/create/', create_article, name='create_article'),
    path('article/view/<int:pk>/', article_view, name='article_view'),
    path('article/edit/<int:pk>/', update_article, name='update_article'),
    path('article/delete/<int:pk>/', delete_article, name='delete_article'),
    path('article/file/create/<int:pk>/', create_article_file, name='create_article_file'),

    path('authors/<int:pk>/', get_article_authors, name='get_article_authors'),
    path('author/add/<int:pk>/', add_author, name='add_author'),
    path('author/edit/<int:pk>/', edit_author, name='edit_author'),
    path('author/delete/<int:pk>/', delete_author, name='delete_author'),

    path('send_message/<int:pk>/<int:user_id>/', send_message, name='send_message'),

    path('sections/', list_sections, name='sections'),
    path('article_types/', article_type_list, name='article_types'),
    path('article_stages/', article_stages_list, name='article_stages'),
    path('article_status/', article_status_list, name='article_status'),
    path('notification_status/', notification_status_list, name='notification_status'),

]
