from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# from .filters import RecipeFilter
from .models import Config
from .serializers import ConfigSerializer


class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    # pagination_class = None
    # filter_backends = (filters.SearchFilter,)
