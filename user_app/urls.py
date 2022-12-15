from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from user_app.views import *

urlpatterns = [
    path('user_dashboard/', user_dashboard, name='dashboard'),
    path('editor_dashboard/', editor_dashboard, name='editor_dashboard'),
    path('reviewer_dashboard/', reviewer_dashboard, name='reviewer_dashboard'),
    path('editor_notifications/', editor_notifications, name='editor_notifications'),
    path('reviewer_notifications/', reviewer_notifications, name='reviewer_notifications'),

    path('editor_check_article/<int:pk>/', editor_check_article, name='editor_check_article'),
    path('editor_submit_result/', editor_submit_result, name='editor_submit_result'),

    path('reviewer_check_article/<int:pk>/', reviewer_check_article, name='reviewer_check_article'),

    path('article_notification/view/<int:pk>/', author_vs_editor_vs_reviewer, name='comment_author_vs_editor'),

    path('load_notif/', load_notification, name='load_notification'),
    path('count_notif/', count_notification, name='count_notification'),
    path('load_reviewers/', load_reviewers, name='load_reviewers'),
    path('sending_reviewer/', sending_reviewer, name='sending_reviewer'),
    path('random_sending_reviewer/', random_sending_reviewer, name='random_sending_reviewer'),

    path('reviewer_confirmed/', reviewer_confirmed, name='reviewer_confirmed'),
    path('reviewer_resubmit/', reviewer_resubmit, name='reviewer_resubmit'),
    path('reviewer_rejected/', reviewer_rejected, name='reviewer_rejected'),

    path('approve_publish/', approve_publish, name='approve_publish'),
    path('editor_resubmit_to_reviewer/', editor_resubmit_to_reviewer, name='editor_resubmit_to_reviewer'),

    path('login/', login_page, name='login'),
    path('logout', logout_user, name='logout'),
    path('register/', register_page, name='register'),
    path('choosen_reviewer_role/', choose_roles, name='choosen_reviewer_role'),
    path('choosen_reviewer_role_list/', reviewer_role_list, name='choosen_reviewer_role_list'),
    path('choosen_reviewer_role_list/<int:pk>/', reviewer_role_list_detail, name='reviewer_role_list_detail'),


    path('edit_profile/', edit_profile, name='edit_profile'),
    path('load_menus/', load_menus, name='load_menus'),
    path('reviewers_list/', reviewers_list, name='reviewers_list'),

    path('countries/', countries_list, name='countries'),
    path('editors/', editors_list, name='editors'),
    path('regions/', regions_list, name='regions'),
    path('genders/', genders_list, name='genders'),
    path('menus/', menus_list, name='menus'),
    path('roles/', roles_list, name='roles'),
    path('scientific_degrees/', scientific_degrees_list, name='scientific_degrees'),
    path('users/', users_list, name='users'),

    #
    # path('admins/', admins, name='admins'),
    # path('users/', users, name='users'),
    # path('users/view/<int:pk>', view_user, name='view_user'),
    # path('users/update/<int:pk>', update_user, name='update_user'),
    # path('users/delete/<int:pk>', delete_user, name='delete_user'),


    path('change_password/', change_password, name='change_password'),
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
