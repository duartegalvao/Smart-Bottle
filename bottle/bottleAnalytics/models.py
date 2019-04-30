from django.db import models
from datetime import datetime


class BottleReading(models.Model):
    temp = models.IntegerField(default=150)
    weight = models.IntegerField(default=150)
    time = models.DateTimeField(default=datetime.now)
