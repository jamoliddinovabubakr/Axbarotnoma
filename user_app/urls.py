from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .views import profile_page, login_page, logout_user, register_page, change_password, edit_profile, admins, users, \
    view_user, update_user, delete_user, get_notifications, view_notification, answer_to_author, get_menus, edit_menu, \
    delete_menu, get_roles, create_role, edit_role, delete_role, get_states, create_state, edit_state, delete_state, \
    get_regions, create_region, edit_region, delete_region, password_reset, profile, load_data_notif

urlpatterns = [
    path('', profile_page, name='profile_page'),
    path('login', login_page, name='login'),
    path('logout', logout_user, name='logout'),
    path('register', register_page, name='register'),
    path('change_password', change_password, name='change_password'),
    path('view/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),

    path('admins/', admins, name='admins'),
    path('users/', users, name='users'),
    path('users/view/<int:pk>', view_user, name='view_user'),
    path('users/update/<int:pk>', update_user, name='update_user'),
    path('users/delete/<int:pk>', delete_user, name='delete_user'),

    path('notifications/', get_notifications, name='notifications'),
    path('load_notif/', load_data_notif, name='load_notif'),
    path('notifications/<int:pk>/view', view_notification, name='view_notification'),
    path('notifications/answer_to_author/<int:pk>', answer_to_author, name='answer_to_author'),

    path('menus/', get_menus, name='menus'),
    # path('menus/create', create_menu, name='create_menu'),
    # path('menus/view/<int:pk>', view_menu, name='view_menu'),
    path('menus/edit/<int:pk>', edit_menu, name='edit_menu'),
    path('menus/delete/<int:pk>', delete_menu, name='delete_menu'),

    # path('genders/', genders, name='genders'),
    # path('genders/create', create_gender, name='create_gender'),
    # path('genders/edit/<int:pk>', edit_gender, name='edit_gender'),
    # path('genders/delete/<int:pk>', delete_gender, name='delete_gender'),

    path('roles/', get_roles, name='roles'),
    path('roles/create', create_role, name='create_role'),
    path('roles/edit/<int:pk>', edit_role, name='edit_role'),
    path('roles/delete/<int:pk>', delete_role, name='delete_role'),

    path('states/', get_states, name='states'),
    path('states/create', create_state, name='create_state'),
    path('states/edit/<int:pk>', edit_state, name='edit_state'),
    path('states/delete/<int:pk>', delete_state, name='delete_state'),

    path('regions', get_regions, name='regions'),
    path('regions/create', create_region, name='create_region'),
    path('regions/edit/<int:pk>', edit_region, name='edit_region'),
    path('regions/delete/<int:pk>', delete_region, name='delete_region'),

    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user_app/register/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="user_app/register/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user_app/register/password_reset_complete.html'),
         name='password_reset_complete'),
]
