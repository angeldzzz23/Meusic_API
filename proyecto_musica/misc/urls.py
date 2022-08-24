
from django.urls import path
from misc import views

urlpatterns = [
    path('genres', views.GenreView.as_view(), name="genres"),
    path('skills', views.SkillView.as_view(), name="skills"),
]
