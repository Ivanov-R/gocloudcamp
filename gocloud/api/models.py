# from django.contrib.auth import get_user_model
# from django.core.validators import MinValueValidator
from django.db import models

# from .models import User

# User = get_user_model()


class Config(models.Model):
    service = models.CharField(max_length=150)
    version = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self) -> str:
        return self.service


class Key(models.Model):
    key = models.CharField(max_length=150)
    value = models.CharField(max_length=150)
    config = models.ForeignKey(Config, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.key
