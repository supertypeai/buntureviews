from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser

from data.api.serializers import (
    AppSerializer,
    AppStoreReviewSerializer,
    PlayStoreReviewSerializer,
    AppStoreReviewBulkSerializer,
)
from .models import App, AppStoreReview, PlayStoreReview, Customer, Watchlist


class AppListCreate(generics.ListCreateAPIView):
    """
    List all snippets or create a new snippet
    """

    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsAdminUser]


class AppDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsAdminUser]


class ReviewListCreate(generics.ListCreateAPIView):
    """
    List all reviews or add a new review
    """

    queryset = AppStoreReview.objects.all()
    serializer_class = AppStoreReviewSerializer


class AppStoreReviewAPIView(generics.CreateAPIView):
    queryset = PlayStoreReview.objects.all()
    serializer_class = AppStoreReviewBulkSerializer

