from django.contrib import admin
from django.urls import path
from michaelscarn import views

urlpatterns = [
    # path('generateData', views.CreatingFakeData.as_view(), name='generateData'),
    path('users', views.CreatingFakeData.as_view(), name='generateData'),
    path('new/<str:id>', views.CreatingFakeData.as_view(), name='generateData'),
]