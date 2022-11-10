from django.urls import path

from .views import APIConfig

urlpatterns = [
    path("config", APIConfig.as_view()),
]
