from rest_framework import serializers
from .models import Rating


# class RatingSerializer(serializers.ModelSerializer):

#     user_name = serializers.CharField(
#         source="user.username",
#         read_only=True
#     )

#     class Meta:
#         model = Rating
#         fields = [
#             "id",
#             "user_name",
#             "rating",
#             "review",
#             "created_at"
#         ]
        
        


class RatingSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Rating
        fields = [
            "id",
            "user_name",
            "rating",
            "review",
            "created_at"
        ]
        

class RatingFarmhouseSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source="user.username", read_only=True)
    user_initial = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = [
            "id",
            "user_name",
            "user_initial",
            "rating",
            "review",
            "created_at"
        ]

    def get_user_initial(self, obj):
        return obj.user.username[0].upper()