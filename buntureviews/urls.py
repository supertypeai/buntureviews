"""buntureviews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from user import views as user_views
from data import views as data_views

urlpatterns = [
    path("", user_views.home, name="home"),
    url(r"^about/$", user_views.AboutView.as_view(), name="about"),
    url(r"^login/$", user_views.login, name="login"),
    url(r"^logout/$", user_views.LogoutView.as_view(), name="logout"),
    url(r"^registration/$", user_views.registration, name="registration"),
    url(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        user_views.account_activate,
        name="activate",
    ),
    url(r"^password/reset/$", user_views.password_reset, name="reset_password"),
    url(
        r"^password/change/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        user_views.password_change,
        name="change_password",
    ),
    url(
        r"^password/change/(?P<uidb64>[0-9A-Za-z_\-]+)/done/$",
        user_views.password_change,
        name="change_password_done",
    ),
    url(r"^add-application/$", data_views.add_application, name="add_application"),
    # path("accounts/", include("django.contrib.auth.urls")),
    url("admin/", admin.site.urls),
    # API URLs
    path("api-auth/", include("rest_framework.urls")),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("api/%s/" % settings.API_VERSION, include("data.urls")),
]
