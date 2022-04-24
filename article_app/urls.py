from django.urls import path, include, re_path
from .views import main_page

urlpatterns = [
    path('', main_page, name='main_page'),
]