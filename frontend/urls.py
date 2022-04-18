from django.urls import path, include, re_path
from .views import main

urlpatterns = [
    path('', main, name='main'),
]