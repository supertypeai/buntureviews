from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    pass

@admin.register(AppStoreReview)
class AppStoreReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(PlayStoreReview)
class PlayStoreReviewAdmin(admin.ModelAdmin):
    pass
