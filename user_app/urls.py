from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .views import login_page, logout_user, register_page, profile_page, change_password, edit_profile, \
    password_reset, profile, admins, users, get_menus, roles, districts, regions, genders, view_user, update_user, \
    delete_user, view_menu, edit_menu, delete_menu, edit_gender, delete_gender

urlpatterns = [
    path('', profile_page, name='profile_page'),
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_page, name='register'),
    path('change_password/', change_password, name='change_password'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),

    path('admins/', admins, name='admins'),
    path('users/', users, name='users'),
    path('users/view/<int:pk>/', view_user, name='view_user'),
    path('users/update/<int:pk>/', update_user, name='update_user'),
    path('users/delete/<int:pk>/', delete_user, name='delete_user'),

    path('menus/', get_menus, name='menus'),
    path('menus/view/<int:pk>/', view_menu, name='view_menu'),
    path('menus/edit/<int:pk>/', edit_menu, name='edit_menu'),
    path('menus/delete/<int:pk>/', delete_menu, name='delete_menu'),

    path('genders/', genders, name='genders'),
    path('genders/edit/<int:pk>/', edit_gender, name='edit_gender'),
    path('genders/delete/<int:pk>/', delete_gender, name='delete_gender'),

    path('roles/', roles, name='roles'),
    path('districts/', districts, name='districts'),
    path('regions/', regions, name='regions'),

    path('edit_profile/', edit_profile, name='edit_profile'),

    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='user_app/register/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="user_app/register/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='user_app/register/password_reset_complete.html'),
         name='password_reset_complete'),
]
