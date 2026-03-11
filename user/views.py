from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
# from farmhouse.authentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import User
from .serializers import (
    RegisterSerializer,
    EmailLoginSerializer,
    UserSerializer,
    ChangePasswordSerializer
)
from django.contrib.auth import login


# ✅ REGISTER
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        user = serializer.save()

        # ⭐ AUTO LOGIN AFTER REGISTER
        login(self.request, user)

# ✅ LOGIN
# class EmailLoginAPIView(generics.GenericAPIView):
#     serializer_class = EmailLoginSerializer
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data["email"]
#         password = serializer.validated_data["password"]

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response(
#                 {"error": "Invalid email or password"},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )

#         user = authenticate(
#             request,
#             username=user.username,   # IMPORTANT
#             password=password
#         )

#         if not user:
#             return Response(
#                 {"error": "Invalid email or password"},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )

#         # 🔥 THIS IS THE KEY LINE
#         login(request, user)

#         return Response({
#             "message": "Login successful",
#             "user": UserSerializer(user).data
#         }, status=status.HTTP_200_OK)


class EmailLoginAPIView(generics.GenericAPIView):
    serializer_class = EmailLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # ✅ authenticate using EMAIL
        user = authenticate(
            request,
            # email=email,
            username=email,
            password=password
        )

        if not user:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # optional: restrict to farmhouse users
        if not user:
            return Response(
                {"error": "You are not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )

        login(request, user)

        return Response({
            "message": "Login successful",
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
        
        
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect("home")

# ✅ PROFILE
# class ProfileAPIView(generics.RetrieveAPIView):
#     serializer_class = UserSerializer

#     def get_object(self):
#         return self.request.user
    
# ✅ CHANGE PASSWORD





# ✅ PROFILE
# class ProfileAPIView(generics.RetrieveAPIView):
#     serializer_class = UserSerializer

#     def get_object(self):
#         return self.request.user


# # ✅ UPDATE PROFILE
# class UpdateProfileAPIView(generics.UpdateAPIView):
#     serializer_class = UserSerializer

#     def get_object(self):
#         return self.request.user







from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
User = get_user_model()
token_generator = PasswordResetTokenGenerator()


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        # ============================
        # 1️⃣ FORGOT PASSWORD
        # ============================
        if "email" in request.data:

            serializer = ForgotPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = User.objects.filter(
                email=serializer.validated_data["email"]
            ).first()

            if not user:
                return Response(
                    {"error": "Email not registered"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            # reset_link = (
            #     f"{settings.LOCAL_URL}"
            #     f"reset-password/{uid}/{token}/"
            # )
            reset_link = (
                f"{settings.LOCAL_URL}"
                f"user/reset-password/?uid={uid}&token={token}"
            )

            send_mail(
                subject="Password Reset",
                message=f"Click below link to reset password:\n{reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return Response(
                {"message": "Password reset link sent to email"},
                status=status.HTTP_200_OK
            )

        # ============================
        # 2️⃣ RESET PASSWORD
        # ============================
        elif "new_password" in request.data:

            uid = request.GET.get("uid")
            token = request.GET.get("token")

            if not uid or not token:
                return Response(
                    {"error": "Reset link is invalid"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = ResetPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            try:
                user_id = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=user_id)
            except Exception:
                return Response(
                    {"error": "Invalid reset link"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not token_generator.check_token(user, token):
                return Response(
                    {"error": "Token expired or invalid"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response(
                {"message": "Password reset successfully"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "Invalid request"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
    
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import update_session_auth_hash

from .serializers import (
    ProfileSerializer,
    ChangePasswordSerializer
)

###################################################
# PROFILE VIEW
###################################################

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ProfileSerializer
    

    def get_object(self):
        return self.request.user


###################################################
# CHANGE PASSWORD VIEW
###################################################

class ChangePasswordAPIView(generics.UpdateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):

        user = self.get_object()

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user.set_password(
            serializer.validated_data["new_password"]
        )
        user.save()

        ###################################################
        # ⭐ VERY IMPORTANT (PREVENT LOGOUT)
        ###################################################
        update_session_auth_hash(request, user)

        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK
        )





        
from django.shortcuts import render

def login_page(request):
    return render(request, "user/login.html")

def register_page(request):
    return render(request, "user/register.html")

def forgot_password_page(request):
    return render(request, "user/forgot_password.html")

def reset_password_page(request):
    return render(request, "user/reset_password.html")




# def profile_page(request):
#     return render(request, "user/profile.html")


from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

@ensure_csrf_cookie
@login_required
def profile_page(request):
    return render(request, "user/profile.html")








# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
from booking.models import Booking
from .serializers import UserBookingSerializer


class UserBookingListAPIView(generics.ListAPIView):

    serializer_class = UserBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Booking.objects.filter(
            user=self.request.user
        ).select_related("farmhouse")
        
        
from booking.serializers import BookingSerializer
class MyBookingDetailAPIView(generics.RetrieveAPIView):

    serializer_class = UserBookingSerializer
    lookup_field = "booking_id"

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

@login_required
def my_bookings_page(request):
    return render(request, "user/user_bookings.html")