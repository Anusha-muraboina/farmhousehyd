from rest_framework import serializers
from .models import (
    Choos_Services,
    Facilities,
    OurFacility,
    WhoWeAre,
    AboutSection,
    AboutFeature,
)


class ChooseServicesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Choos_Services
        fields = [
            "id",
            "title",
            "description",
            "icon",
            "image",
            "Slot_position",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None



class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = [
            "id",
            "name",
        ]


class OurFacilitySerializer(serializers.ModelSerializer):
    facilities = FacilitiesSerializer(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = OurFacility
        fields = [
            "id",
            "main_title",
            "description",
            "image",
            "facilities",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None



class WhoWeAreSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = WhoWeAre
        fields = [
            "id",
            "title",
            "description",
            "icon",
            "image",
            "Slot_position",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None



class AboutFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutFeature
        fields = [
            "id",
            "icon",
            "title",
        ]
class AboutSectionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    features = AboutFeatureSerializer(many=True)

    class Meta:
        model = AboutSection
        fields = [
            "id",
            "title_tag",
            "main_title",
            "description",
            "image",
            "video",
            "features",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return ""

    def get_video(self, obj):
        request = self.context.get("request")
        if obj.video and request:
            return request.build_absolute_uri(obj.video.url)
        return ""



# ======================================

from rest_framework import serializers
from .models import AboutWhoWeAre


class AboutWhoWeAreSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = AboutWhoWeAre
        fields = [
            "id",
            "small_title",
            "main_title",
            "mission_title",
            "mission_description",
            "difference_title",
            "difference_description",
            "image",
            "button_text",
            "is_active",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


