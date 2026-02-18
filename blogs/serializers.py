from rest_framework import serializers
from .models import *


class BlogCategorySerializer(serializers.ModelSerializer):
    blog_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogCategory
        fields = ["id", "name", "slug", "blog_count"]


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ["id", "name", "slug"]


class BlogListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category = BlogCategorySerializer()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "image",
            "short_description",
            "published_at",
            "read_time",
            "category",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return ""


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = ["id", "name", "comment", "created_at"]


class BlogDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category = BlogCategorySerializer()
    tags = BlogTagSerializer(many=True)
    comments = BlogCommentSerializer(many=True)

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "image",
            "content",
            "views",
            "read_time",
            "published_at",
            "category",
            "tags",
            "comments",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return ""
    def get_content(self, obj):
        return str(obj.content) 