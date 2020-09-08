from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from rest_framework import generics, viewsets, views
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from data.api.serializers import *
from .models import App, AppStoreReview, Customer, Watchlist
from common.mails.mail_base import EmailHandler
from data.forms.application import AddApplicationForm


@login_required(login_url="/login/")
def add_application(request):
    context, customer = {}, None
    try:
        customer = request.user.customer
    except:
        pass
    context["customer"] = customer
    if request.method == "GET":
        if customer is not None:
            watchlist_filter_data = Watchlist.objects.filter(customer=customer)
        if not watchlist_filter_data.exists():
            pass
        else:
            apps = watchlist_filter_data.first().apps.all()
            context["apps"] = apps
        context["form"] = AddApplicationForm()
        return render(request, "addApplication.html", context)
    elif request.method == "POST":
        form = AddApplicationForm(request.POST)
        context["form"] = form
        if form.is_valid():
            app_id = request.POST["app_id"]
            country = request.POST["country"]
            apps = [{"app_id": app_id, "primary_country": country}]
            response, data = App.create_multiple_app(apps)
            appName = data[0].appName
            if response is False:
                context["error"] = data
            if response is True and len(data) == 0:
                context["error"] = "App list is empty"

            if response is True and len(data) > 0 and customer is not None:
                instance = None
                try:
                    instance = customer.watchlist
                except:
                    instance = None

                if instance is None:
                    instance = Watchlist.objects.create(
                        country=country, customer=customer
                    )

                old_data = [app for app in instance.apps.all()]
                instance.apps.clear()
                data = old_data + data
                instance.apps.set(data)

                context["success"] = "App '{0}' added in watchlist".format(appName)
                context["form"] = AddApplicationForm()
                apps = instance.apps.all()
                context["apps"] = apps
                return render(request, "addApplication.html", context)
            else:
                apps = instance.apps.all()
                context["apps"] = apps
                return render(request, "addApplication.html", context)
        else:
            watchlist_filter_data = Watchlist.objects.filter(customer=customer)
            apps = watchlist_filter_data.first().apps.all()
            context["apps"] = apps
            return render(request, "addApplication.html", context)

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
        return Watchlist.objects.filter(customer__user=user)

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

