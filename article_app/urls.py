from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from .views import main_page, my_articles, create_article, update_my_article, add_author, edit_author, delete_author, \
    delete_myarticle, get_category, edit_category, delete_category, create_category, create_magazine, get_magazines, edit_magazine, post_detail, about_journal, \
    talabnoma, magazine_detail

urlpatterns = [
    path('', main_page, name='main_page'),
    path('about_journal/', about_journal, name='about_journal'),
    path('talabnoma/', talabnoma, name='talabnoma'),
    path('contact/', TemplateView.as_view(template_name="contact.html"), name='contact'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),


    path('articles/', my_articles, name='my_articles'),
    path('article/create', create_article, name='create_article'),
    path('article/edit/<int:pk>/', update_my_article, name='update_my_article'),
    path('article/delete/<int:pk>/', delete_myarticle, name='delete_myarticle'),

    path('author/<int:pk>/', add_author, name='add_author'),
    path('author/edit/<int:pk>/', edit_author, name='edit_author'),
    path('author/delete/<int:pk>/', delete_author, name='delete_author'),

    path('magazines/', get_magazines, name='get_magazines'),
    path('magazine/create', create_magazine, name='create_magazine'),
    path('magazine/view/<int:pk>/', magazine_detail, name='view_magazine'),
    path('magazine/edit/<int:pk>', edit_magazine, name='edit_magazine'),

    path('categories/', get_category, name='get_category'),
    path('category/create/', create_category, name='create_category'),
    path('category/edit/<int:pk>/', edit_category, name='edit_category'),
    path('category/delete/<int:pk>/', delete_category, name='delete_category'),

]
