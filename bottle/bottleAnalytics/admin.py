from django.contrib import admin

from . import models


admin.site.register(models.BottleReading)
admin.site.register(models.UserSettings)
