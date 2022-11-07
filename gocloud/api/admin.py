from django.contrib import admin

from .models import Config, Key

admin.site.register(Config)
admin.site.register(Key)
