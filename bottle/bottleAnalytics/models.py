from django.db import models
from datetime import datetime, date
from solo.models import SingletonModel


ACTIVITY_LEVEL_CHOICES = (
    ('SE', 'Sedentary'),
    ('LA', 'Low Active'),
    ('AC', 'Active'),
    ('VA', 'Very Active'),
)

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class BottleReading(models.Model):
    temp = models.IntegerField(default=150)
    weight = models.IntegerField(default=150)
    time = models.DateTimeField(default=datetime.now)


class UserSettings(SingletonModel):
    birth_date = models.DateField(default=None, blank=True, null=True)
    activity_level = models.CharField(max_length=2,
                                      choices=ACTIVITY_LEVEL_CHOICES,
                                      default='LA')
    sex = models.CharField(max_length=1,
                           choices=SEX_CHOICES,
                           default='M')

    def get_age(self):
        if self.birth_date is None:
            return 30
        else:
            today = date.today()
            return today.year - self.birth_date.year
