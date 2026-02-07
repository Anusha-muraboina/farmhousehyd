from django.urls import path
from .views import *

urlpatterns = [

    path('register/', RegisterAPIView.as_view(), name='user-register'),

    path('login/', EmailLoginAPIView.as_view(), name='user-login'),
    
    path("logout/", logout_view, name="logout"),

    # path('profile/', ProfileAPIView.as_view(), name='user-profile'),

    # path('profile/update/', UpdateProfileAPIView.as_view(), name='user-profile-update'),

    path(
        "profile/",
        ProfileAPIView.as_view(),
        name="profile-api"
    ),

    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change-password-api"
    ),
    path(
    "forgot-password/",
    PasswordResetView.as_view(),
    name="forgot-password"
    ),

    path("profile_page/", profile_page, name="profile_page"),


    path(
        "my-bookings/",
        UserBookingListAPIView.as_view(),
        name="user-bookings"
    ),

    path(
        "my-bookings/<str:booking_id>/",
        MyBookingDetailAPIView.as_view(),
    ),
    path(
        "my-bookings-page/",
        my_bookings_page,
        name="my-bookings-page"
    ),

    path("login-page/", login_page, name="login-page"),
    path("register-page/", register_page, name="register-page"),
    path("forgot-password-page/", forgot_password_page, name="forgot-password-page"),
    path("reset-password/", reset_password_page, name="reset-password-page"),
    
]
