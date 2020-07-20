from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator


class App(models.Model):
    appName = models.CharField(max_length=60)
    store = models.CharField(max_length=30)
    appid = models.CharField(max_length=60)
    publisher = models.CharField(max_length=60)
    category = models.CharField(max_length=30)
    similar = models.ManyToManyField("self", blank=True)


class AppStoreReview(models.Model):
    author = models.CharField(max_length=60)
    version = models.CharField(max_length=10)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(blank=True, null=True, max_length=60)
    content = models.TextField()
    country = models.CharField(max_length=2)
    app = models.ForeignKey("App", null=True, on_delete=models.SET_NULL)


class PlayStoreReview(AppStoreReview):
    authorImg = models.URLField()
    reviewedAt = models.DateTimeField()
    replyContent = models.TextField()
    repliedAt = models.DateTimeField()

    class Meta:
        ordering = ["-reviewedAt"]


class Customer(models.Model):
    accountName = models.CharField(max_length=60)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()


class Watchlist(models.Model):
    app = models.ManyToManyField("App")
    country = models.CharField(max_length=2)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)

