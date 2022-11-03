# from django.contrib.auth import get_user_model
# from django.core.validators import MinValueValidator
from django.db import models

# from .models import User

# User = get_user_model()


class Data(models.Model):
    key1 = models.CharField(max_length=150)
    key2 = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name


class Config(models.Model):
    service = models.CharField(max_length=150, unique=True)
    data = models.ForeignKey(
        Data, on_delete=models.CASCADE, related_name="data_keys")
    version = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self) -> str:
        return self.service
