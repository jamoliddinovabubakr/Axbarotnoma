from django.urls import path, include, re_path
from .views import login_page, logout_user, register_page, main_page, cabinet_page

urlpatterns = [
    path('', main_page, name='main_page'),
    path('cabinet/', cabinet_page, name='cabinet_page'),
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_page, name='register'),
]