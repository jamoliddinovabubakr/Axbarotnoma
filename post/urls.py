from django.urls import path

from post.views import *

urlpatterns = [
    # path('post/create/', create_post, name='create_post'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    # path('post/edit/<int:pk>', edit_post, name='edit_post'),
    # path('post/delete/<int:pk>', delete_post, name='delete_post'),
]
