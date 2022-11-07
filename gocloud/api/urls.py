from django.urls import include, path

# from .views import ConfigViewSet
from .views import APIConfig

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()

# router.register("config", ConfigViewSet)


urlpatterns = [
    # path("", include(router.urls)),
    path("config/", APIConfig.as_view()),
]
