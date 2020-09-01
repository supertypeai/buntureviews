from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from rest_framework import generics, viewsets, views
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from data.api.serializers import *
from .models import App, AppStoreReview, Customer, Watchlist
from common.mails.mail_base import EmailHandler
from data.forms.application import AddApplicationForm


@login_required(login_url="/login/")
def add_application(request):
    context = {}
    if request.method == "GET":
        context["form"] = AddApplicationForm()
        return render(request, "addApplication.html", context)


class CustomerCreateAPIView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class WatchlistAPIViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        customer = user.customer
        return Watchlist.objects.filter(customer=customer)

    def get_serializer_class(self):
        if self.action == "list" or self.action == "create":
            return WatchListSerializer
        else:
            return WatchListDetailUpdateSerializer


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
                "USER_EMAIL": "rongbong@boximail.com",
                "PASSWORD_URL": "localhost:8080/password-reset",
            }
            mail_handler = EmailHandler(
                "Test mail subject", mail_body, ["rongbong@boximail.com",]
            )
            response = mail_handler.customer_login_email()
            message = (
                "Email send successfully" if response is True else "Email not sent!"
            )
        except:
            message = "Email internal error"

        return Response({"message": message})

