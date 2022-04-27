from django.urls import path, include, re_path
from django.views.generic import TemplateView
from .views import login_page, logout_user, register_page, profile_page, settings_page, change_password, edit_profile

urlpatterns = [
    path('', profile_page, name='profile_page'),
    path('settings/', settings_page, name='settings'),
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_page, name='register'),
    path('change_password/', change_password, name='change_password'),
    path('edit_profile/', edit_profile, name='edit_profile'),
]
