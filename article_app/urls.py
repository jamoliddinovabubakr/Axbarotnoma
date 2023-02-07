from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('', main_page, name='main_page'),
    path('contact/', contact, name='contact'),
    path('about_journal/', about_journal, name='about_journal'),
    path('editor_board/', editor_board, name='editor_board'),
    path('guide_for_authors/', guide_for_authors, name='guide_for_authors'),
    path('load_sidebar_menus/', load_sidebar_menus, name='load_sidebar_menus'),
    path('load_navbar_menus/', load_navbar_menus, name='load_navbar_menus'),

    path('article/create/', create_article, name='create_article'),
    path('article/view/<int:pk>/', article_view, name='article_view'),
    path('article/edit/<int:pk>/', update_article, name='update_article'),
    path('article/delete/<int:pk>/', delete_article, name='delete_article'),
    path('article/file/create/<int:pk>/', create_article_file, name='create_article_file'),

    path('authors/<int:pk>/', get_article_authors, name='get_article_authors'),
    path('author/add/<int:pk>/', add_author, name='add_author'),
    path('author/edit/<int:pk>/', edit_author, name='edit_author'),
    path('author/delete/<int:pk>/', delete_author, name='delete_author'),

    # Article Status
    path('article_status/', article_status_list, name='article_status_list'),
    path('article_status_update/<int:pk>/', article_status_update, name='article_status_update'),
    path('article_status_delete/<int:pk>/', article_status_delete, name='article_status_delete'),

    path('send_message/<int:pk>/<int:user_id>/', send_message, name='send_message'),

    # Sections
    path('sections/', list_sections, name='sections'),
    path('section_delete/<int:pk>/', section_delete, name='section-delete'),
    path('section_update/<int:pk>/', section_update, name='section-update'),
    path('section_create', section_create, name='section-create'),

    # Article type
    path('article_types/', article_type_list, name='article_types'),
    path('article_types_delete/<int:pk>/', article_type_delete, name='article_type_delete'),
    path('article_type_update/<int:pk>/', article_type_update, name='article_type_update'),
    path('article_type_create', article_type_create, name='article_type_create'),

    # Article stage
    path('article_stages/', article_stages_list, name='article_stages'),
    path('article_stages_delete/<int:pk>/', article_stages_delete, name='article_stages_delete'),
    path('article_stages_update/<int:pk>/', article_stages_update, name='article_stages_update'),
    path('artilce_stages_create/', article_stages_create, name='article_stages_create'),

    # Notification status 
    path('notification_status/', notification_status_list, name='notification_status'),
    path('notification_status_delete/<int:pk>/', notification_status_delete, name='notification_delete'),
    path('notification_status_update/<int:pk>/', notification_status_update, name='notification_update'),
    path('notification_status_create/', notification_status_create, name='notification_create')

]
