from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_bytes, force_text
from django.views import View
from django.template import loader
from django.contrib import messages
from django.urls import reverse
from rest_framework import views, viewsets
from user.forms.login import LoginForm
from user.forms.registration import RegistrationForm
from user.forms.password_reset.reset_init import ResetInitForm
from user.forms.password_reset.password_change import PasswordChangeForm
from user.models import User
from data.models import Customer, Watchlist
from user.token import get_token

# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name = "home.html"


@login_required(login_url="/login/")
def home(request):
    template = loader.get_template("home.html")
    context, customer = {}, None
    try:
        customer = request.user.customer
    except:
        pass

    context["customer"] = customer
    if customer is not None:
        watchlist_filter_data = Watchlist.objects.filter(customer=customer)
        if not watchlist_filter_data.exists():
            pass
        else:
            apps = watchlist_filter_data.first().apps.all()
            context["apps"] = apps

    return render(request, "home.html", context)


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        context = {}
        context["form"] = form
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(username=email, password=password)
            if user is not None and user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse("home"))
            else:
                user_filter_data = User.objects.filter(username=email)
                if (
                    user_filter_data.exists()
                    and user_filter_data.first().is_active is False
                ):
                    context["errors"] = "Active your account before login"
                elif not user_filter_data.exists():
                    context["errors"] = "User doesn't exists"
                return render(request, "login.html", context)
        context["form_errors"] = form.errors
        return render(request, "login.html", context)
    elif request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        form = LoginForm()
        return render(request, "login.html", {"form": form})


def registration(request):
    context = {}

    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        form = RegistrationForm()
        context["form"] = form
        return render(request, "registration.html", context)
    elif request.method == "POST":
        form = RegistrationForm(request.POST)
        context["form"] = form
        if form.is_valid():
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]

            user_filter_data = User.objects.filter(email=email)
            if user_filter_data.exists():
                # context["form"] = form
                context["errors"] = "User email already exists"
                return render(request, "registration.html", context)
            else:
                data_obj = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "username": email,
                    "is_active": False,
                    "is_staff": False,
                    "password": password,
                    "confirm_password": confirm_password,
                }
                print(data_obj)

                response, data = Customer.create_customer(data_obj)
                if response is False:
                    context["errors"] = data
                    return render(request, "registration.html", context)
                else:
                    context[
                        "success"
                    ] = "Account activation link has been sent to your email. Please active account before login"
                    form = RegistrationForm()
                    context["form"] = form
                    return render(request, "registration.html", context)

        return render(request, "registration.html", context)


def account_activate(request, **kwargs):
    context = {}
    if request.method == "GET":
        uid = kwargs["uidb64"]
        token = kwargs["token"]
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user_filter_data = User.objects.filter(id=uid)
            if not user_filter_data.exists():
                context["error"] = "User not found"
                return render(request, "account_active.html", context)
            else:
                user = user_filter_data.first()
                if get_token.check_token(user, token):
                    user.is_active = True
                    user.save()
                    context["success"] = "Your account successfully activated"
                    context["user"] = user
                    return render(request, "account_active.html", context)
                else:
                    context["error"] = "Activation link invalid"
                    return render(request, "account_active.html", context)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return render(request, "account_active.html", context)


def password_reset(request):
    context = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        form = ResetInitForm()
        context["form"] = form
        return render(request, "password_reset_init.html", context)
    elif request.method == "POST":
        form = ResetInitForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            user_filter_data = User.objects.filter(email=email)
            if not user_filter_data.exists():
                context["errors"] = "User not found"
            else:
                response, data = User.send_password_reset_link(user_filter_data.first())
                if response is False:
                    context["errors"] = data
                else:
                    context["success"] = data
            form = ResetInitForm()
            context["form"] = form
        else:
            context["errors"] = "Form is not valid"

        return render(request, "password_reset_init.html", context)


def password_change(request, **kwargs):
    context = {}
    if request.method == "GET":
        uid = kwargs["uidb64"]
        token = kwargs["token"]
        context["submission_link"] = "/password/change/" + uid + "/done/"

        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user_filter_data = User.objects.filter(id=uid)

            if not user_filter_data.exists():
                context["errors"] = "User not found"
                return render(request, "password_change.html", context)
            else:
                user = user_filter_data.first()
                if get_token.check_token(user, token):
                    context["form"] = PasswordChangeForm()

                    return render(request, "password_change.html", context)
                else:
                    context["errors"] = "Password Reset link invalid"
                    return render(request, "password_change.html", context)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return render(request, "password_change.html", context)
    elif request.method == "POST":
        uid = kwargs["uidb64"]

        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user_filter_data = User.objects.filter(id=uid)
            if not user_filter_data.exists():
                context["errors"] = "User not found"
                return render(request, "password_change.html", context)
            else:
                user = user_filter_data.first()
                form = PasswordChangeForm(request.POST)
                password = request.POST["password"]
                confirm_password = request.POST["confirm_password"]

                if confirm_password != password:
                    context["errors"] = "Password & Confirm Password is not same"
                    context["form"] = PasswordChangeForm()
                    return render(request, "password_change.html", context)
                else:
                    user.set_password(password)
                    user.save()
                    context[
                        "success"
                    ] = "Your password reset successfully, login with new password"
                    context["form"] = PasswordChangeForm()
                    return render(request, "password_change.html", context)

                return render(request, "password_change.html", context)

            return render(request, "password_change.html", context)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            context["errors"] = "Internal Error"
            context["form"] = PasswordChangeForm()
            return render(request, "password_change.html", context)


class AboutView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name = "about.html"


class RegistrationView(TemplateView):
    template_name = "registration/registration.html"


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("/login/")

