from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from rest_framework import urls, schemas
from cmdb.views import index


urlpatterns = [
    path('sti/', RedirectView.as_view(url=settings.URL_PATH_PREFIX)),
    path(
        settings.URL_PATH_PREFIX[1:],
        include(
            [
                path('oauth/', include('social_django.urls', namespace='social')),
                path('admin/login/', RedirectView.as_view(url=settings.URL_PATH_PREFIX + 'oauth/login/suap/')),
                path('admin/', admin.site.urls),
                path('markdownx/', include('markdownx.urls')),
                path('', index),
            ]
        )
    ),
    path('', RedirectView.as_view(url=settings.URL_PATH_PREFIX)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
