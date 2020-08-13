from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework import serializers
from data.models import *
from user.api.serializers import UserMinimalSerializer
from user.models import User
import logging, uuid

logger = logging.getLogger(__name__)

class CustomerSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer()

    def create(self, validated_data):
        user = validated_data.pop("user")
        password = str(uuid.uuid4().hex)
        user = User.objects.create_user(username=user["username"], email=user["email"], password=password)
        customer_instance = user.customer
        if "accountName" in validated_data:
            customer_instance.accountName = validated_data["accountName"]
            customer_instance.save()

        return customer_instance

    class Meta:
        model = Customer
        fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = "__all__"


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

    def create(self, validated_data):
        return super().create(validated_data)


class AppStoreReviewBulkSerializer(serializers.ModelSerializer):
    reviews = serializers.ListField(write_only=True)

    def create(self, validated_data):
        reviews = validated_data.pop("reviews")
        review_instances = []
        for review in reviews:
            app_filter_data = App.objects.filter(id=int(review["app"]))
            if not app_filter_data.exists():
                raise serializers.ValidationError("App not found")
            review["app"] = app_filter_data.first()
            review_instances.append(AppStoreReview(**review))
        try:
            AppStoreReview.objects.bulk_create(review_instances)
            return AppStoreReview.objects.all()[0]
        except:
            raise serializers.ValidationError("Internal Error")

    class Meta:
        model = AppStoreReview
        fields = "__all__"
        extra_kwargs = {
            "reviews": {"write_only": True}
        }
        read_only_fields = ("author","version","rating","title","content","country","app",)
