from rest_framework import serializers
from .models import (
    Banner,
    Location,
    Amenity,
    Farmhouse,
    FarmhouseImage,
)
from blogs.models import *


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
        fields = ["id", "name", "slug"]


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name", "icon_class"]


class FarmhouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmhouseImage
        fields = ["image", "is_primary"]


class FarmhouseSerializer(serializers.ModelSerializer):
        # 🔥 THIS IS THE KEY LINE
    amenities = AmenitySerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()
    images = FarmhouseImageSerializer(many=True, read_only=True)
    class Meta:
        model = Farmhouse
        fields = [
            "id",
            "title",
            "user",
            "slug",
            "location",
            "address",
            "description",
            "short_description",
            "price_per_day",
            "primary_image",
            "bedrooms",
            "ac_bedrooms",
            "halls",
            "amenities",
            "images",
            
        ]

    # def get_primary_image(self, obj):
    #     image = obj.images.filter(is_primary=True).first()
    #     if image:
    #         return image.image.url
    #     return ""
    def get_primary_image(self, obj):
        request = self.context.get("request")

        # ✅ get primary image from related images
        image = obj.images.filter(is_primary=True).first()

        if image and request:
            return request.build_absolute_uri(image.image.url)

        return None


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