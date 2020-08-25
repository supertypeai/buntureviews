from django.db import models
from user.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

from .utils import validate_appid, _guess_store, create_review_data
from common.mails.mail_base import EmailHandler
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

    def save(self, *args, **kwargs):
        response = validate_appid(self.appid, self.primaryCountry)
        if response is not None and self.id is None:
            self.appName, self.store, self.publisher, self.category = response
            self.primaryCountry = self.primaryCountry.lower()
            super().save(*args, **kwargs)

    @classmethod
    def create_multiple_app(cls, apps):
        app_list = []
        for app in apps:
            if "app_id" not in app:
                return False, "app_id not found"

            if "primary_country" not in app:
                return False, "primary_country not found"

            app_id, country = app["app_id"], app["primary_country"]
            app_filter_data = cls.objects.filter(appid=app_id, primaryCountry=country)
            if not app_filter_data.exists():
                store_response = _guess_store(app_id)
                if store_response in ["AppStore", "PlayStore"]:
                    app_instance = cls.objects.create(
                        appid=app_id, primaryCountry=country
                    )
                    try:
                        review_create_response, data = create_review_data(
                            app_id, country, store_response, app_instance
                        )
                        if review_create_response == 404:
                            pass
                        elif review_create_response == 400:
                            app_instance.delete()
                            return False, "Review not created, try again!"
                        elif review_create_response == 201:
                            app_list.append(app_instance)
                    except expression as identifier:
                        app_instance.delete()
                        return False, "Internal Error"
            else:
                app_list.append(app_filter_data.first())

        return True, app_list


class AppReviewBaseAbstract(models.Model):
    author = models.CharField(max_length=120, blank=True, null=True)
    version = models.CharField(max_length=15, blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(blank=True, null=True, max_length=200)
    content = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    app = models.ForeignKey(
        App, related_name="%(class)s_reviews", null=True, on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True


class AppStoreReview(AppReviewBaseAbstract):
    appid = models.CharField(null=True, max_length=220)


class PlayStoreReview(AppReviewBaseAbstract):
    authorImg = models.URLField(null=True)
    reviewedAt = models.DateTimeField()
    replyContent = models.TextField(blank=True, null=True)
    repliedAt = models.DateTimeField(blank=True, null=True)
    reviewId = models.CharField(_("Review ID"), max_length=220, blank=True, null=True)
    thumbsUpCount = models.IntegerField(default=0)

    class Meta:
        ordering = ["-reviewedAt"]


class Customer(models.Model):
    accountName = models.CharField(max_length=60)
    user = models.OneToOneField(User, related_name="customer", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @classmethod
    def create_customer(cls, validated_data):
        user = validated_data.pop("user")
        user_filter_data = User.objects.filter(username=user["username"])
        if user_filter_data.exists():
            return False, "User already exists"

        password = str(uuid.uuid4().hex)
        user_instance = User.objects.create_user(
            username=user["username"], email=user["email"], password=password
        )
        customer_instance = cls.objects.create(
            user=user_instance, accountName=validated_data.get("accountName")
        )

        mail_body = {
            "USERNAME": customer_instance.user.username,
            "USER_EMAIL": customer_instance.user.email,
            "PASSWORD_URL": "localhost:8080/password-reset",
        }
        try:
            mail_handler = EmailHandler(
                "Customer account created", mail_body, [customer_instance.user.email,]
            )
            response = mail_handler.customer_login_email()
        except:
            pass

        return True, customer_instance


class Watchlist(models.Model):
    apps = models.ManyToManyField(App)
    country = models.CharField(max_length=2)
    customer = models.ForeignKey(
        "Customer", related_name="watch_lists", on_delete=models.CASCADE
    )


# @receiver(post_save, sender=User)
# def create_customer(sender, instance, created, **kwargs):
#     if created:
#         Customer.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_customer(sender, instance, **kwargs):
#     instance.customer.save()

