# from django.contrib.auth import get_user_model
# from django.core.validators import MinValueValidator
from django.db import models

# from .models import User

# User = get_user_model()


class KeyValue(models.Model):
    key = models.CharField(max_length=150)
    value = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.key


class Config(models.Model):
    service = models.CharField(max_length=150)
    data = models.ManyToManyField(KeyValue, through='ConfigKeyValue')
    version = models.DecimalField(max_digits=3, decimal_places=1, default=0.1)

    class Meta:
        ordering = ["-service"]
        constraints = [
            models.UniqueConstraint(
                fields=["service", "version"], name="unique version"
            )
        ]

    def __str__(self) -> str:
        return f'{self.service} {self.version}'


class ConfigKeyValue(models.Model):
    config = models.ForeignKey(
        Config, on_delete=models.CASCADE)
    key_value = models.ForeignKey(
        KeyValue, on_delete=models.CASCADE)

    # class Meta:
    #     ordering = ["-recipe"]
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["recipe", "tag"], name="unique tag"
    #         )
    #     ]

    def __str__(self):
        return f'{self.config} {self.key_value}'
