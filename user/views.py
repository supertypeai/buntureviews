from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.views import View
from django.template import loader
from django.contrib import messages
from django.urls import reverse
from rest_framework import views, viewsets
from user.forms.login import LoginForm
from user.forms.registration import RegistrationForm
from user.models import User
from data.models import Customer

# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name = "home.html"


@login_required(login_url="/login/")
def home(request):
    text = " welcome to Home"
    template = loader.get_template("home.html")
    context = {"text": text}
    return HttpResponse(template.render(context, request))


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
        form = LoginForm()
        return render(request, "login.html", {"form": form})


def registration(request):
    context = {}

    if request.method == "GET":
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
                if first_name is None or len(first_name) == 0:
                    context["errors"] = "First Name can't be empty"
                    return render(request, "registration.html", context)
                if last_name is None or len(last_name) == 0:
                    context["errors"] = "Last Name can't be empty"
                    return render(request, "registration.html", context)
                if password != confirm_password:
                    context["errors"] = "Password & Confirmation password is not same"
                    return render(request, "registration.html", context)
                data_obj = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "username": email,
                    "is_active": False,
                    "is_staff": False,
                }
                instance = User.objects.create(**data_obj)
                instance.set_password(password)
                instance.save()

                customer = Customer(user=instance, accountName=instance.username).save()

                context[
                    "success"
                ] = "Account activation link has been sent to your email. Please active account before login"
                form = RegistrationForm()
                context["form"] = form
                return render(request, "registration.html", context)

        return render(request, "registration.html", context)


class AboutView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name = "about.html"


class RegistrationView(TemplateView):
    template_name = "registration/registration.html"


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("/login/")

