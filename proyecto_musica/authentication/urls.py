from authentication import views
from django.urls import path
urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name="register"),
    path('login', views.LoginAPIView.as_view(), name="login"),
    path('user', views.AuthUserAPIView.as_view(), name="user"),
    path('verifyemail/', views.VerifyEmail.as_view(), name="verifyemail"),

    path('user/<str:id>', views.AuthUserAPIView.as_view(), name='user_by_id')
]
