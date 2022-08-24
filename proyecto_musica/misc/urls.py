
from django.urls import path
from misc import views

urlpatterns = [
    path('genres', views.GenresView.as_view(), name="genres"),
]
