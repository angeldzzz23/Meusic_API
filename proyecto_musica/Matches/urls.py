from django.contrib import admin
from django.urls import path
from Matches import views

#SeeUserView
urlpatterns = [
    # path('profile', views.SeeProfileOfUserView.as_view(), name="profile"),
    path('', views.MatchesView.as_view(), name="matches"),
    path('unmatch/<str:id>', views.UnMatchView.as_view(), name="like"),

]
