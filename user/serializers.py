from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

from rest_framework import serializers
from booking.models import Booking

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone',
            'password',
            'password2',
     
        )

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)


# from rest_framework import serializers

class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phone',
            'assignedpermission'
        )


# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField()
#     new_password = serializers.CharField()






from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data






from rest_framework import serializers
from .models import User


class ProfileSerializer(serializers.ModelSerializer):
    wallet_balance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone",
            "wallet_balance",
          
        ]

        read_only_fields = ["email"]  
        # 🔥 NEVER allow email change easily
    def get_wallet_balance(self, obj):

        if hasattr(obj, "wallet"):
            return obj.wallet.balance

        return 0

# serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data




class UserBookingSerializer(serializers.ModelSerializer):

    farmhouse_name = serializers.CharField(
        source="farmhouse.title",
        read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            "booking_id",
            "farmhouse_name",
            "check_in",
            "check_out",
            "guest_count",
            "extra_guest_count",
            "total_amount",
            "remaining_amount",
            "disc_price",
            "status",
            "payment_status",
            "payment_method",
            "created_at",
            
        ]

