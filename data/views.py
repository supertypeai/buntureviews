from django.core.mail import send_mail
from rest_framework import generics, viewsets, views
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from data.api.serializers import (
    CustomerSerializer,
    WatchListSerializer,
    AppSerializer,
    AppStoreReviewSerializer,
    #PlayStoreReviewSerializer,
    AppStoreReviewBulkSerializer,
)
from .models import App, AppStoreReview, Customer, Watchlist
from common.mails.mail_base import EmailHandler


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


class EmailCheckAPIView(views.APIView):
    def get(self, request, format=None):
        message = ""
        try:
            mail_body = {
                "USERNAME": "devadmin",
                "USER_EMAIL": "faltu-kaj@boximail.com",
                "PASSWORD_URL": "localhost:8080/password-reset"
            }
            mail_handler = EmailHandler("Test mail subject", mail_body, ["rongbong@boximail.com",])
            response = mail_handler.customer_login_email()
            message = "Email send successfully" if response is True else "Email not sent!"    
        except:
            message = "Email internal error"
        
        return Response({"message": message})
        
        

