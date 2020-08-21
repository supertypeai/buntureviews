from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework import status
from data.models import *
from data.utils import *
from user.api.serializers import UserMinimalSerializer
from user.models import User
import logging, uuid

logger = logging.getLogger(__name__)


class CustomerSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer()

    def create(self, validated_data):
        response, data = Customer.create_customer(validated_data)
        if response is False:
            raise serializers.ValidationError(
                {"detail": data}, code=status.HTTP_404_NOT_FOUND
            )
        return data

    class Meta:
        model = Customer
        fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    total_apps = serializers.SerializerMethodField()
    apps = serializers.ListField(write_only=True)

    def get_customer(self, model):
        return {"id": model.customer.id, "username": model.customer.user.username}

    def get_total_apps(self, model):
        return model.apps.count()

    def create(self, validated_data):
        user = self.context.get("request").user
        if user.customer is None:
            raise serializers.ValidationError(
                {"detail": "User customer profile not found"},
                code=status.HTTP_404_NOT_FOUND,
            )
        customer = user.customer
        apps = validated_data.pop("apps")
        if len(apps) == 0:
            raise serializers.ValidationError({"detail": "App list can't be empty"})

        country = validated_data.get("country")
        response, data = App.create_multiple_app(apps)
        if response is False:
            raise serializers.ValidationError(
                {"detail": data}, code=status.HTTP_404_NOT_FOUND
            )

        instance = Watchlist.objects.create(country=country, customer=customer)
        instance.apps.set(data)
        return instance

    class Meta:
        model = Watchlist
        fields = "__all__"
        extra_kwargs = {
            "apps": {"write_only": True},
            "customer": {"read_only": True},
            "total_apps": {"read_only": True},
        }


class WatchListDetailUpdateSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        customer = instance.customer
        apps, app_list = instance.apps.all(), []
        for app in apps:
            app_dict = {
                "id": app.id,
                "appid": app.appid,
                "primaryCountry": app.primaryCountry,
                "appName": app.appName,
                "store": app.store,
                "total_review": app.playstorereview_reviews.count()
                if app.store == "PlayStore"
                else app.appstorereview_reviews.count(),
            }
            app_list.append(app_dict)
        return {
            "id": instance.id,
            "country": instance.country,
            "customer": {
                "id": customer.id,
                "username": customer.user.username,
                "email": customer.user.email,
                "accountName": customer.accountName,
            },
            "apps": app_list,
        }

    def update(self, instance, validated_data):
        apps = validated_data.pop("apps")
        instance.country = validated_data.get("country", instance.country)

        instance.save()
        return instance

    class Meta:
        model = Watchlist
        fields = "__all__"
        read_only_fields = ("customer",)


class AppSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        similar = None
        if "similar" in validated_data:
            similar = validated_data.pop("similar")
        try:
            validation_response = validate_appid(
                validated_data["appid"], validated_data["primaryCountry"]
            )
            if validation_response is None:
                raise serializers.ValidationError({"error": "Internal Error"})

            instance = App(
                appid=validated_data["appid"],
                primaryCountry=validated_data["primaryCountry"],
            )
            instance.save()
            if similar is not None and len(similar) > 0:
                instance.similar.set(similar)
                instance.save()
            return instance
        except:
            raise serializers.ValidationError({"error": "Internal Error"})

    class Meta:
        model = App
        fields = "__all__"
        read_only_fields = ("appName", "store", "publisher", "category")


class AppFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ("id", "appName", "store", "primaryCountry")


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


# class PlayStoreReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PlayStoreReview

#     def create(self, validated_data):
#         return super().create(validated_data)


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
        extra_kwargs = {"reviews": {"write_only": True}}
        read_only_fields = (
            "author",
            "version",
            "rating",
            "title",
            "content",
            "country",
            "app",
        )
