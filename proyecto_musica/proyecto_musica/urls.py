"""proyecto_musica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin

from django.urls import path, include
from django.conf import settings #3
from django.conf.urls.static import static  #4
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include("authentication.urls")),
    path('api/upload/', include('api.urls')),
    path('api/misc/', include('misc.urls')),
    path('api/search/', include('search.urls')),
    path('api/chat/', include('chat.urls')),
    path("chat/", include('chat.urls',namespace='chat')),
]
# Serving the media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
