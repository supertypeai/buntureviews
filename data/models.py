from django.db import models
from user.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

from .utils import validate_appid
import uuid


class App(models.Model):
    appid = models.CharField(max_length=60)
    primaryCountry = models.CharField(max_length=2)
    appName = models.CharField(max_length=60)
    store = models.CharField(max_length=30)
    publisher = models.CharField(max_length=60)
    category = models.CharField(max_length=30)
    similar = models.ManyToManyField("self", blank=True)

    class Meta:
        unique_together = ("appid", "primaryCountry")

    def __str__(self):
        return f"App {self.appName} on {self.store}"

    # def clean(self, *args, **kwargs):
    #     pass

    # def fill_data(self):
    #     print("Filling data for", self.appid)
    #     self.appName, self.store, self.publisher, self.category = validate_appid(
    #         self.appid, self.primaryCountry
    #     )

    def save(self, *args, **kwargs):
        """
        Automatically populate the rest of fields taking the appid
        and also create an entry in Watchlist with the primary market.
        Extracts the first batch of reviews from API and create the 
        corresponding entries in the review tables
        """

        self.appName, self.store, self.publisher, self.category = validate_appid(
            self.appid, self.primaryCountry
        )
        self.primaryCountry = self.primaryCountry.lower()
        super().save(*args, **kwargs)


class AppStoreReview(models.Model):
    author = models.CharField(max_length=60)
    version = models.CharField(max_length=10)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(blank=True, null=True, max_length=60)
    content = models.TextField()
    country = models.CharField(max_length=2)
    app = models.ForeignKey(App, null=True, on_delete=models.SET_NULL)


class PlayStoreReview(AppStoreReview):
    authorImg = models.URLField()
    reviewedAt = models.DateTimeField()
    replyContent = models.TextField()
    repliedAt = models.DateTimeField()

    class Meta:
        ordering = ["-reviewedAt"]


class Customer(models.Model):
    accountName = models.CharField(max_length=60)
    user = models.OneToOneField(User, related_name="customer", on_delete=models.CASCADE)

    @classmethod
    def create_customer(cls, validated_data):
        user = validated_data.pop("user")
        user_filter_data = User.objects.filter(username=user["username"])
        if user_filter_data.exists():
            return False, "User already exists"
        
        password = str(uuid.uuid4().hex)
        user_instance = User.objects.create_user(username=user["username"], email=user["email"], password=password)
        customer_instance = cls.objects.create(user=user_instance, accountName=validated_data.get("accountName"))

        return True, customer_instance


class Watchlist(models.Model):
    app = models.ManyToManyField("App")
    country = models.CharField(max_length=2)
    customer = models.ForeignKey("Customer", related_name="watch_lists", on_delete=models.CASCADE)


# @receiver(post_save, sender=User)
# def create_customer(sender, instance, created, **kwargs):
#     if created:
#         Customer.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_customer(sender, instance, **kwargs):
#     instance.customer.save()





