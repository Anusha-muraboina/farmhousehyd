from decimal import Decimal
from datetime import timedelta
from farmhouse.models import FarmhousePricing




from decimal import Decimal
from datetime import timedelta

def calculate_booking_cost(farmhouse, check_in, check_out, extra_guest_count=0):

    total = Decimal("0.00")
    current = check_in

    pricing = farmhouse.pricing

    # ✅ dynamic weekend days (default Sat+Sun)
    weekend_days = farmhouse.weekend_days or [5, 6]

    while current < check_out:

        ################################################
        # ✅ 1. OFFER PRICE (HIGHEST PRIORITY)
        ################################################
        offer = farmhouse.offers.filter(
            start_date__lte=current,
            end_date__gte=current
        ).order_by("-is_sale", "price").first()

        if offer:
            day_price = Decimal(offer.price)

        else:
            ################################################
            # ✅ 2. NORMAL / WEEKEND PRICE
            ################################################
            day = current.weekday()  # Monday=0

            if day in weekend_days:
                day_price = Decimal(pricing.weekend_price)
            else:
                day_price = Decimal(pricing.normal_day_price)

        total += day_price
        current += timedelta(days=1)

    ################################################
    # ✅ EXTRA GUEST COST (PER NIGHT)
    ################################################
    nights = (check_out - check_in).days

    extra_cost = (
        Decimal(extra_guest_count)
        * Decimal(pricing.extra_guest_price or 0)
        * Decimal(nights)
    )

    return total + extra_cost










# def calculate_booking_cost(farmhouse, check_in, check_out, extra_guest_count=0):

#     total = Decimal("0.00")
#     current = check_in

#     while current < check_out:

#         # ✅ 1. CHECK OFFER PRICE FIRST
#         offer = farmhouse.offers.filter(
#             start_date__lte=current,
#             end_date__gte=current
#         ).order_by("-is_sale", "price").first()

#         if offer:
#             day_price = offer.price

#         else:
#             # ✅ 2. FALLBACK TO NORMAL/WEEKEND
#             pricing = farmhouse.pricing

#             if current.weekday() >= 5:
#                 day_price = pricing.weekend_price
#             else:
#                 day_price = pricing.normal_day_price

#         total += Decimal(day_price)

#         current += timedelta(days=1)

#     # ✅ EXTRA GUEST COST (per night)
#     nights = (check_out - check_in).days

#     extra_cost = (
#         Decimal(extra_guest_count)
#         * farmhouse.pricing.extra_guest_price
#         * nights
#     )

#     return total + extra_cost






























































# def calculate_booking_cost(farmhouse, check_in, check_out, extra_guest_count=0):

#     pricing = farmhouse.pricing

#     total = Decimal("0.00")
#     current = check_in

#     while current < check_out:

#         if current.weekday() >= 5:
#             total += pricing.weekend_price
#         else:
#             total += pricing.normal_day_price

#         current += timedelta(days=1)

#     nights = (check_out - check_in).days

#     extra_cost = (
#         Decimal(extra_guest_count)
#         * pricing.extra_guest_price
#         * nights
#     )

#     return total + extra_cost
