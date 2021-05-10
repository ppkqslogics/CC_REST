"""user URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from userapp.views.views import welcome_page
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from userapp import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('ccapi-admin/', admin.site.urls),
    path('', views.welcome_page, name="welcome"),
    path('userapp/', include('userapp.urls')),
    path('profile_app/', include('profile_app.urls')),
    path('contact_app/', include('contact_app.urls')),
    path('moments_app/', include('moments_app.urls')),
    path('setting_app/', include('setting_app.urls')),
    path('token/refresh/', TokenRefreshView.as_view(), name='token')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
