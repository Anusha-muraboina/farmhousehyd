from rest_framework import serializers
from .models import (
    Banner,
    Location,
    Amenity,
    Farmhouse,
    FarmhouseImage,
    FarmhousePricing,
    FarmhouseFacilities,
    Thingstocarry,
    Propertyrules,
    HomePopup
)
from django.db.models import Avg
from blogs.models import *
from booking.models import FarmhousePaymentPolicy
from rating.serializers import RatingSerializer

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"
    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name","meta_title","meta_description", "meta_keywords" ,"slug"]


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name", "icon_class"]



class ThingstocarrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Thingstocarry
        fields = ["id", "name" ,"slot_position","active"]
        
        
class PropertyrulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propertyrules
        fields = ["id", "name" ,"slot_position","active"]
        


# serializers.py

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmhouseFacilities
        fields = ["id", "name","active"]   # add fields you have


# class FarmhouseImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FarmhouseImage
#         fields = ["image", "is_primary"]






class FarmhousePaymentPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmhousePaymentPolicy
        fields = [
            "allow_pay_at_farmhouse",
            "allow_partial_payment",
            "allow_full_payment",
        ]


class FarmhouseImageSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = FarmhouseImage
        fields = ["image", "is_primary"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class FarmhousePricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmhousePricing
        fields = "__all__"

from datetime import date
class FarmhouseSerializer(serializers.ModelSerializer):
    pricing = FarmhousePricingSerializer(read_only=True)
        # 🔥 THIS IS THE KEY LINE
    amenities = AmenitySerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()
    images = FarmhouseImageSerializer(many=True, read_only=True)
    facilities = FacilitySerializer(many=True, read_only=True)
    
    thingstocarry = ThingstocarrySerializer(many=True, read_only=True)
    properyrules = PropertyrulesSerializer(many=True, read_only=True)
    location = serializers.SerializerMethodField()
    # payment_policy = FarmhousePaymentPolicySerializer(read_only=True)
    payment_policy = serializers.SerializerMethodField()


       # ⭐ ADD THESE
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()
    
    
    dynamic_price = serializers.SerializerMethodField()
    current_offer = serializers.SerializerMethodField()
    class Meta:
        model = Farmhouse
        fields = [
            "id",
            "title",
            "user",
            "slug",
            "location",
            "address",
            "guest_count",
            "extra_guest_count",
            "description",
            "short_description",
            "price_per_day",
            "primary_image",
            "bedrooms",
            "ac_bedrooms",
            "halls",
            "breakfast_dinner_available",
            "food_menu",
            "amenities",
            "thingstocarry",
            "properyrules",
            "facilities",
            "images",
            "pricing",
            "payment_policy",
            "map_embed",
            "Slot_position",
            
            # rating fields
            "average_rating",
            "total_reviews",
            "ratings",
            
            "dynamic_price",
            "current_offer",
            
        ]
        
    # def get_dynamic_price(self, obj):
    #     return obj.get_price_by_date(date.today())

    def get_dynamic_price(self, obj):

        today = date.today()

        offer = obj.offers.filter(
            start_date__lte=today,
            end_date__gte=today,
            is_sale=True
        ).first()

        if offer:
            return float(offer.price)

        return 0
    
    def get_current_offer(self, obj):

        offers = obj.offers.all().values(
            "title",
            "price",
            "start_date",
            "end_date"
        )

        return list(offers)
    # def get_current_offer(self, obj):

    #     offer = obj.offers.filter(
    #         start_date__lte=date.today(),
    #         end_date__gte=date.today()
    #     ).first()

    #     if offer:
    #         return {
    #             "title": offer.title,
    #             "price": offer.price,
    #             "start_date": offer.start_date,   # ✅ ADD
    #             "end_date": offer.end_date        # ✅ ADD
    #         }

    #     return None

    # def get_primary_image(self, obj):
    #     image = obj.images.filter(is_primary=True).first()
    #     if image:
    #         return image.image.url
    #     return ""
    def get_primary_image(self, obj):
        request = self.context.get("request")

        # ✅ Try primary image first
        image = obj.images.filter(is_primary=True).first()

        # ✅ If no primary → take first image
        if not image:
            image = obj.images.first()

        if image and request:
            return request.build_absolute_uri(image.image.url)

        return None
    # def get_primary_image(self, obj):
    #     request = self.context.get("request")

    #     # ✅ get primary image from related images
    #     image = obj.images.filter(is_primary=True).first()

    #     if image and request:
    #         return request.build_absolute_uri(image.image.url)

    #     return None
    def get_location(self, obj):
        if obj.location:
            return {
                "name": obj.location.name,
                "slug": obj.location.slug
            }
        return None
    def get_payment_policy(self, obj):

        policy = getattr(obj, "payment_policy", None)

        # ✅ DEFAULT POLICY
        default_policy = {
            "allow_pay_at_farmhouse": True,
            "allow_partial_payment": True,
            "allow_full_payment": True,  # ALWAYS TRUE
        }

        if not policy:
            return default_policy

        return {
            "allow_pay_at_farmhouse": policy.allow_pay_at_farmhouse,
            "allow_partial_payment": policy.allow_partial_payment,
            "allow_full_payment": True, 
        }

    # ⭐ Average Rating
    def get_average_rating(self, obj):

        avg = obj.ratings.aggregate(
            avg=Avg("rating")
        )["avg"]

        if avg:
            return round(avg, 1)

        return 0


    # ⭐ Total Reviews
    def get_total_reviews(self, obj):

        return obj.ratings.count()
    
    def get_ratings(self, obj):

        ratings = obj.ratings.select_related("user").all()

        return RatingSerializer(
            ratings,
            many=True
        ).data

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "image",
            "short_description",
            "published_at",
            "read_time"
             
        ]
    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
    
    


class HomePopupSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomePopup
        fields = [
            "image",
            "is_active"
        ]