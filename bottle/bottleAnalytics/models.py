from django.db import models
from datetime import datetime
from solo.models import SingletonModel


class BottleReading(models.Model):
    temp = models.IntegerField(default=150)
    weight = models.IntegerField(default=150)
    time = models.DateTimeField(default=datetime.now)


class UserSettings(SingletonModel):
    birth_date = models.DateField(default=None, blank=True, null=True)
    weight = models.FloatField(default=65)
