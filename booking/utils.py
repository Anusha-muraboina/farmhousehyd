from decimal import Decimal
from datetime import timedelta
from farmhouse.models import FarmhousePricing


def calculate_booking_cost(farmhouse, check_in, check_out, extra_guest_count=0):

    pricing = farmhouse.pricing

    total = Decimal("0.00")
    current = check_in

    while current < check_out:

        if current.weekday() >= 5:
            total += pricing.weekend_price
        else:
            total += pricing.normal_day_price

        current += timedelta(days=1)

    nights = (check_out - check_in).days

    extra_cost = (
        Decimal(extra_guest_count)
        * pricing.extra_guest_price
        * nights
    )

    return total + extra_cost
