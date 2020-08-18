from django.urls import path, re_path, include, reverse
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r"watch-lists", views.WatchlistAPIViewSet, 'watch_lists')

urlpatterns = [
    path("customer/create", views.CustomerCreateAPIView.as_view()),
    path("app", views.AppListCreate.as_view()),
    # eg. http://127.0.0.1:8000/api/app/1
    path("app/<int:pk>", views.AppDetail.as_view()),
    # eg. http://127.0.0.1:8000/api/reviews/itunes/1
    path(
        "reviews/itunes/<int:pk>",
        views.ReviewListCreate.as_view(),
        name="itunes-review-list-create",
    ),
    path(
        "mail-check/",
        views.EmailCheckAPIView.as_view(),
        name="mail-check",
    ),
    re_path(r"^", include(router.urls)),
]
