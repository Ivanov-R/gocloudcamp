from django.contrib import admin

from .models import Config, ConfigKeyValue, KeyValue

admin.site.register(Config)
admin.site.register(KeyValue)
admin.site.register(ConfigKeyValue)
