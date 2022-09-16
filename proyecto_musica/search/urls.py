from django.urls import path

from search import views

urlpatterns = [

path('gender', views.SearchGender.as_view(), name="gender"),
path('skills', views.searchSkills.as_view(), name="skills"),


]
