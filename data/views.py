from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from data.api.serializers import (
    CustomerSerializer,
    WatchListSerializer,
    AppSerializer,
    AppStoreReviewSerializer,
    PlayStoreReviewSerializer,
    AppStoreReviewBulkSerializer,
)
from .models import App, AppStoreReview, PlayStoreReview, Customer, Watchlist


class CustomerCreateAPIView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class WatchlistAPIViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = (IsAuthenticated,)


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

