from django.db import models


class KeyValue(models.Model):
    key = models.CharField(max_length=150)
    value = models.CharField(max_length=150)

    class Meta:
        ordering = ["-key"]
        constraints = [
            models.UniqueConstraint(
                fields=["key", "value"], name="unique key_value"
            )
        ]

    def __str__(self) -> str:
        return f'{self.key} {self.value}'


class Config(models.Model):
    service = models.CharField(max_length=150, null=True, blank=True,)
    data = models.ManyToManyField(KeyValue, through='ConfigKeyValue')
    version = models.DecimalField(max_digits=3, decimal_places=1, default=0.1)

    class Meta:
        ordering = ["-service"]

    def __str__(self) -> str:
        return f'{self.service} {self.version}'


class ConfigKeyValue(models.Model):
    config = models.ForeignKey(
        Config, on_delete=models.CASCADE, related_name='key_values')
    key_value = models.ForeignKey(
        KeyValue, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-config"]
        constraints = [
            models.UniqueConstraint(
                fields=["config", "key_value"], name="unique config key_value"
            )
        ]

    def __str__(self):
        return f'{self.config} {self.key_value}'
