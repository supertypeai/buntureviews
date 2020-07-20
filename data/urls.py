from django.urls import path
from . import views

urlpatterns = [
    path("app", views.AppListCreate.as_view()),
]
