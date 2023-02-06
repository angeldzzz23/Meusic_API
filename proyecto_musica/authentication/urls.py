from authentication import views
from django.urls import path
urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name="register"),
    path('login', views.LoginAPIView.as_view(), name="login"),
    path('user', views.AuthUserAPIView.as_view(), name="user"),
    path('verifyemail/', views.VerifyEmail.as_view(), name="verifyemail"),
    path('forgotpassword/', views.ForgotPassword.as_view(), name='forgotpassword'),
    path('forgotpassword/verify', views.VerifyForgotPassword.as_view(), name='verify'),
    path('user/<str:id>', views.AuthUserAPIView.as_view(), name='user_by_id'),
    path('refreshWC', views.CookieTokenRefreshView.as_view(), name="token_refresh"),
    path('refresh', views.CookieTokenRefreshView2.as_view(), name="token_refresh3"),
    path('isactive', views.verifyIsSetUp.as_view(), name="isactive")



]
