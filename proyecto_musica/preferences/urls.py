"""preferences URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from preferences import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gender', views.PreferenceGenderView.as_view(), name="gender"),
    #path('genders/<str:id>', views.PreferenceGenderView.as_view(), name="genders_by_id"),
    path('skill', views.PreferenceSkillView.as_view(), name="skill"),
    #path('skills/<str:id>', views.PreferenceSkillView.as_view(), name='skills_by_id'),
    path('genre', views.PreferenceGenreView.as_view(), name="genre"),
    #path('genres/<str:id>', views.PreferenceGenreView.as_view(), name="genres_by_id"),
    path('age', views.PreferenceAgeView.as_view(), name="age"),
    # path('distance', views.Distance.as_view(), name="distance"),
    # path('globally', views.Globally.as_view(), name="globally"),
]
