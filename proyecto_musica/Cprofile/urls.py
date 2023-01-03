"""Cprofile URL Configuration

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
from django.urls import path
from Cprofile import views


urlpatterns = [
    path('skills', views.CUserSkills.as_view()),
    path('genres', views.CUserGenres.as_view()),
    path('artists', views.CUserArtists.as_view()),
    path('youtube', views.CUserYoutubeVideos.as_view()),
    path('vimeo', views.CUserVimeoVideos.as_view()),
    path('video', views.CUserPersonalVideos.as_view()),
    path('images', views.CUserPersonalImages.as_view()),
    path('about_me', views.CUserAboutMe.as_view()),
    path('username', views.CUsername.as_view()),
    path('name', views.Cname.as_view()),
    path('dob', views.Cdob.as_view()),
    path('gender', views.CUserGender.as_view())
]
