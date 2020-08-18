from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "accountName")

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "country", "customer",)

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    pass

@admin.register(AppStoreReview)
class AppStoreReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "version", "rating", "title", "app")


@admin.register(PlayStoreReview)
class PlayStoreReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "version", "rating", "app")
