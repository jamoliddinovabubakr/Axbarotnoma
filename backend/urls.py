from django.urls import path, include, re_path
from .views import home, login_page, logout_user, register_page

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_page, name='register'),
]