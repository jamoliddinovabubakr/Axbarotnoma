from django.urls import path

from journal.views import *

urlpatterns = [
    path('dashboard/', journal_dashboard, name='journal_dashboard'),
    path('create/', create_journal, name='create_journal'),
    path('view/<int:pk>/', journal_detail, name='view_journal'),
    path('edit/<int:pk>/', edit_journal, name='edit_journal'),
    path('delete/<int:pk>/', delete_journal, name='delete_journal'),
    path('split_pages/<int:pk>/', split_journal_pages, name='split_journal_pages'),
    # path('about_journal/', about_journal, name='about_journal'),
    path('journals_list/', journals_list, name='journals_list'),
    path('article_view/<int:pk>/', journal_article_view, name='journal_article_view'),
]
