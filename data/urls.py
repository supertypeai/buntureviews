from django.urls import path
from . import views

urlpatterns = [
    path("app", views.AppListCreate.as_view()),
    # eg. http://127.0.0.1:8000/api/app/1
    path("app/<int:pk>", views.AppDetail.as_view()),
    # eg. http://127.0.0.1:8000/api/reviews/itunes/1
    path("reviews/itunes/<int:pk>", views.ReviewListCreate.as_view()),
]
