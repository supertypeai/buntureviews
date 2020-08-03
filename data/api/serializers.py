from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework import serializers

from ..models import App, AppStoreReview, PlayStoreReview


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = "__all__"
        read_only_fields = ("appName", "store", "publisher", "category")


class BulkCreateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]
        print(result)

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise ValidationError(e)

        return result


class AppStoreReviewSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = AppStoreReview(**validated_data)

        if isinstance(self._kwargs["data"], dict):
            instance.save()

        return instance

    class Meta:
        model = AppStoreReview
        fields = "__all__"
        list_serializer_class = BulkCreateListSerializer


# class AppStoreReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AppStoreReview
#         fields = "__all__"


class PlayStoreReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayStoreReview
