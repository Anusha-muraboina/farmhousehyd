

from rest_framework import serializers
from booking.models import Booking

class BookingSerializer(serializers.ModelSerializer):
    farmhouse_name = serializers.CharField(source="farmhouse.name", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "booking_id",
            "farmhouse_name",
            "guest_name",
            "guest_email",
            "guest_phone",
            "check_in",
            "check_out",
            "total_amount",
            "wallet_used",
            "status",
            "payment_status",
            "created_at",
        ]