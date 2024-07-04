from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"books", views.BookViewSet, basename="book")

urlpatterns = [path("", include(router.urls))]
