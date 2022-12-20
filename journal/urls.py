from django.urls import path

from journal.views import create_journal, split_pdf, journal_detail, get_journal, about_journal, journals_number, \
    journal_article, edit_journal, delete_journal, journal_view, journal_dashboard

urlpatterns = [
    path('dashboard/', journal_dashboard, name='journal_dashboard'),
    path('create/', create_journal, name='create_journal'),
    path('view/<int:pk>/', journal_detail, name='view_journal'),
    path('edit/<int:pk>/', edit_journal, name='edit_journal'),

    path('about_journal/', about_journal, name='about_journal'),
    path('list_journals/', journals_number, name='all_journals_son'),
    path('journals/', get_journal, name='get_journals'),
    path('journal_view/<int:pk_article>/', journal_article, name='journal_article'),
    # path('splitpdf/', split_pdf, name='split_pdf'),
    path('delete_journal/<int:delete_journal_id>/', delete_journal, name='delete_journal'),
    path('jorunal_view/<int:journal_view_id>/', journal_view, name='journal_view')
]
