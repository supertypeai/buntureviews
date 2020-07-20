from rest_framework import generics

from data.api.serializers import (
    AppSerializer,
    AppStoreReviewSerializer,
    PlayStoreReviewSerializer,
)
from .models import App, AppStoreReview, PlayStoreReview


class AppListCreate(generics.ListCreateAPIView):
    """
    App List Create
    """

    queryset = App.objects.all()
    serializer_class = AppSerializer

