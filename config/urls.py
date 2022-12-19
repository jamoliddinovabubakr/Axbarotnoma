from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from article_app.views import set_language

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

urlpatterns += i18n_patterns(

    path('admin/', admin.site.urls),
    path('', include('article_app.urls')),
    path('profile/', include('user_app.urls')),
    path('journal/', include('journal.urls')),
    path('post/', include('post.urls')),
    path("set_language/<str:language>", set_language, name="set-language"),
    prefix_default_language=False,
)
urlpatterns += [
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'user_app.views.handler404'
