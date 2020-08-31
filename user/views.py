from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.template import loader
from django.urls import reverse
from rest_framework import views, viewsets
from user.forms.login import LoginForm

# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name = "home.html"


@login_required
def home(request):
    text = " welcome to Home"
    template = loader.get_template("home.html")
    context = {"text": text}
    return HttpResponse(template.render(context, request))


class AboutView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name = "about.html"


class RegistrationView(TemplateView):
    template_name = "registration/registration.html"


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("/login")


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/"

    # def get(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return HttpResponseRedirect("/")

    #     return HttpResponseRedirect("/login")

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("home"))
            return HttpResponseRedirect(reverse("login"))

