from rest_framework import serializers

from ..models import App, AppStoreReview, PlayStoreReview


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = "__all__"
        read_only_fields = ("appName", "store", "publisher", "category")


class AppStoreReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppStoreReview
        fields = "__all__"


class PlayStoreReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayStoreReview
