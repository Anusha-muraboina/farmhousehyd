from rest_framework import serializers
from .models import ContactInfo, ContactMessage
from farmhouse.models import Farmhouse


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = "__all__"


class FarmhouseSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmhouse
        fields = ["id", "title"]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            "farmhouse",
            "name",
            "phone",
            "email",
            "message"
        ]
