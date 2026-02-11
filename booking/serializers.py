from rest_framework import serializers
from decimal import Decimal
from datetime import date

from .models import Booking
from farmhouse.models import Farmhouse
from coupon.models import Coupon
from .utils import calculate_booking_cost
from .models import BlockedDate


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = "__all__"

        read_only_fields = [
            "id",
            "booking_id",
            "payment_status",
            "status",
            "transaction_id",
            "payment_id",
            "remaining_amount",
            "sub_total",
            "total_amount",
        ]

    ###################################
    # VALIDATION
    ###################################
    def validate(self, data):

        check_in = data["check_in"]
        check_out = data["check_out"]
        farmhouse = data["farmhouse"]

        if check_out <= check_in:
            raise serializers.ValidationError(
                "Checkout must be after checkin"
            )
            # raise serializers.ValidationError({
            #     "non_field_errors": ["Checkout must be after check-in."]
            # })


        ###################################
        # EXISTING BOOKINGS
        ###################################

        # overlapping = Booking.objects.filter(
        #     farmhouse=farmhouse,
        #     # status__in=["confirmed"],
        #     status__in=["pending","confirmed"],
        #     check_in__lt=check_out,
        #     check_out__gt=check_in
        # )

        # if overlapping.exists():
        #     raise serializers.ValidationError(
        #         "These dates are already booked."
        #     )

        ###################################
        # BLOCKED DATES
        ###################################

        blocked = BlockedDate.objects.filter(
            farmhouse=farmhouse,
            start_date__lt=check_out,
            end_date__gt=check_in
        )


        if blocked.exists():
            raise serializers.ValidationError(
                "These dates are blocked."
            )

        return data


    # def validate(self, data):

    #     check_in = data["check_in"]
    #     check_out = data["check_out"]
    #     farmhouse = data["farmhouse"]

    #     if check_in < date.today():
    #         raise serializers.ValidationError("Past date not allowed")

    #     if check_out <= check_in:
    #         raise serializers.ValidationError("Invalid checkout")

    #     overlapping = Booking.objects.filter(
    #         farmhouse=farmhouse,
    #         status__in=["pending", "confirmed"],
    #         check_in__lt=check_out,
    #         check_out__gt=check_in
    #     )

    #     if overlapping.exists():
    #         raise serializers.ValidationError("Dates already booked")

    #     return data

    ###################################
    # CREATE BOOKING
    ###################################

    # def create(self, validated_data):

    #     farmhouse = validated_data["farmhouse"]

    #     total = calculate_booking_cost(
    #         farmhouse=farmhouse,
    #         check_in=validated_data["check_in"],
    #         check_out=validated_data["check_out"],
    #         extra_guest_count=validated_data.get("extra_guest_count", 0)
    #     )

    #     discount = Decimal("0.00")

    #     # coupon = validated_data.get("coupon_applied")

    #     # if coupon and coupon.is_valid():
    #     #     discount = coupon.calculate_discount(total)

    #     final_total = total - discount
    #     validated_data["sub_total"] = total
    #     validated_data["disc_price"] = discount
    #     validated_data["total_amount"] = final_total
    #     validated_data["remaining_amount"] = final_total
    #     validated_data["payment_status"] = "pending"
    #     validated_data["status"] = "pending"

    #     booking = Booking.objects.create(**validated_data)

    #     return booking
        # booking = Booking.objects.create(

        #     sub_total=total,
        #     disc_price=discount,
        #     total_amount=final_total,
        #     remaining_amount=final_total,

        #     payment_status="pending",
        #     status="pending",

        #     **validated_data
        # )

        # return booking



# booking/serializers.py

from .models import BlockedDate

class BlockedDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlockedDate
        fields = ["start_date", "end_date"]


# cancellation



from rest_framework.generics import ListAPIView
from .models import *


class CancelReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancelReason
        fields = ["id", "reason"]

