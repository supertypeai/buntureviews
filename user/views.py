from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import views, viewsets

# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"


class RegistrationView(TemplateView):
    template_name = "registration.html"


class LoginView(TemplateView):
    template_name = "login.html"
