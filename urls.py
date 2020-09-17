from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('login/', auth_views.login, name='login'),
    # path('logout/', auth_views.logout, name='logout'),
    # path('oauth/', include('social_django.urls', namespace='social')), 
    # path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url='/admin')),
    # path('', include('social_django.urls'), name='social'),
    path('login/', auth_views.LoginView, name='login'),
    path('logout/', auth_views.LogoutView, name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
]
