from django.urls import path
from .views import *

urlpatterns = [

    path('register/', RegisterAPIView.as_view(), name='user-register'),

    path('login/', EmailLoginAPIView.as_view(), name='user-login'),
    
    path("logout/", logout_view, name="logout"),

    path('profile/', ProfileAPIView.as_view(), name='user-profile'),

    path('profile/update/', UpdateProfileAPIView.as_view(), name='user-profile-update'),

    path('change-password/', ChangePasswordAPIView.as_view(), name='user-change-password'),
    path(
    "forgot-password/",
    PasswordResetView.as_view(),
    name="forgot-password"
    ),

    path("login-page/", login_page, name="login-page"),
    path("register-page/", register_page, name="register-page"),
    path("forgot-password-page/", forgot_password_page, name="forgot-password-page"),
    path("reset-password/", reset_password_page, name="reset-password-page"),
    
]
