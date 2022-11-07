from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ConfigViewSet

router = DefaultRouter()

router.register("config", ConfigViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
