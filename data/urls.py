from django.urls import path
from . import views

urlpatterns = [
    path("app", views.AppListCreate.as_view()),
    path("app/<int:pk>", views.AppDetail.as_view()),
]
