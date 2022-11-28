from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from user_app.views import *

urlpatterns = [
    path('user_dashboard/', dashboard, name='dashboard'),
    path('editor_dashboard/', editor_dashboard, name='editor_dashboard'),
    path('reviewer_dashboard/', reviewer_dashboard, name='reviewer_dashboard'),
    path('editor_notifications/', editor_notifications, name='editor_notifications'),
    path('reviewer_notifications/', reviewer_notifications, name='reviewer_notifications'),
    path('editor_check_article/<int:pk>/', editor_check_article, name='editor_check_article'),
    path('reviewer_check_article/<int:pk>/', reviewer_check_article, name='reviewer_check_article'),

    path('article_notification/view/<int:pk>/', author_vs_editor_vs_reviewer, name='comment_author_vs_editor'),

    path('load_notif/', load_notification, name='load_notification'),
    path('count_notif/', count_notification, name='count_notification'),
    path('load_reviewers/', load_reviewers, name='load_reviewers'),
    path('sending_reviewer/', sending_reviewer, name='sending_reviewer'),

    path('login/', login_page, name='login'),
    path('logout', logout_user, name='logout'),
    path('register/', register_page, name='register'),
    path('choose_role/', choose_roles, name='choose_role'),

    # path('change_password', change_password, name='change_password'),
    # path('view/', profile, name='profile'),
    # path('edit_profile/', edit_profile, name='edit_profile'),
    #
    # path('admins/', admins, name='admins'),
    # path('users/', users, name='users'),
    # path('users/view/<int:pk>', view_user, name='view_user'),
    # path('users/update/<int:pk>', update_user, name='update_user'),
    # path('users/delete/<int:pk>', delete_user, name='delete_user'),

    
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
