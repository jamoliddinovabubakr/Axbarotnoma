from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from user_app.views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login_page, name='login'),
    path('logout', logout_user, name='logout'),
    path('register/', register_page, name='register'),
    # path('change_password', change_password, name='change_password'),
    # path('view/', profile, name='profile'),
    # path('edit_profile/', edit_profile, name='edit_profile'),
    #
    # path('admins/', admins, name='admins'),
    # path('users/', users, name='users'),
    # path('users/view/<int:pk>', view_user, name='view_user'),
    # path('users/update/<int:pk>', update_user, name='update_user'),
    # path('users/delete/<int:pk>', delete_user, name='delete_user'),
    #
    path('notifications/', get_notifications, name='notifications'),
    # path('load_notif/', load_data_notif, name='load_notif'),
    # path('count_notif/', count_notif, name='count_notif'),
    # path('get_review_view_notification/', get_review_view_notification, name='get_review_view_notification'),
    # path('notification/<int:pk>/view', view_notification, name='view_notification'),
    # path('notification/answer_to_author/<int:pk>', answer_to_author, name='answer_to_author'),
    # path('send_to_review/<int:article_id>', send_to_review, name='send_to_review'),
    #
    # path('review_view_notifications/', review_notifications, name='review_view_notifications'),
    # path('review_view_notification/<int:pk>/view', review_view_notification, name='review_notification_view'),
    #
    # path('menus/', get_menus, name='menus'),
    # # path('menus/create', create_menu, name='create_menu'),
    # # path('menus/view/<int:pk>', view_menu, name='view_menu'),
    # path('menus/edit/<int:pk>', edit_menu, name='edit_menu'),
    # path('menus/delete/<int:pk>', delete_menu, name='delete_menu'),
    #
    # # path('genders/', genders, name='genders'),
    # # path('genders/create', create_gender, name='create_gender'),
    # # path('genders/edit/<int:pk>', edit_gender, name='edit_gender'),
    # # path('genders/delete/<int:pk>', delete_gender, name='delete_gender'),
    #
    # path('roles/', get_roles, name='roles'),
    # path('roles/create', create_role, name='create_role'),
    # path('roles/edit/<int:pk>', edit_role, name='edit_role'),
    # path('roles/delete/<int:pk>', delete_role, name='delete_role'),
    #
    # path('states/', get_states, name='states'),
    # path('states/create', create_state, name='create_state'),
    # path('states/edit/<int:pk>', edit_state, name='edit_state'),
    # path('states/delete/<int:pk>', delete_state, name='delete_state'),
    #
    # path('regions', get_regions, name='regions'),
    # path('regions/create', create_region, name='create_region'),
    # path('regions/edit/<int:pk>', edit_region, name='edit_region'),
    # path('regions/delete/<int:pk>', delete_region, name='delete_region'),
    #
    # path('password_reset/', password_reset, name='password_reset'),
    # path('password_reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(
    #          template_name='user_app/register/password_reset_done.html'),
    #      name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name="user_app/register/password_reset_confirm.html"),
    #      name='password_reset_confirm'),
    # path('reset/done/',
    #      auth_views.PasswordResetCompleteView.as_view(
    #          template_name='user_app/register/password_reset_complete.html'),
    #      name='password_reset_complete'),
]
