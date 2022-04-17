from django.urls import path, include, re_path
from .views import home, login_page

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_page, name='login'),
]