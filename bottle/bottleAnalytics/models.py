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

SCORE_CHOICES = (
    ('A', 'Ideal hydration!'),
    ('B', 'Slightly lower than expected...'),
    ('C', 'Lower than expected...'),
    ('D', 'Too low hydration.'),
    ('E', 'No values available.'),
    ('O', 'Might be over-hydrating!'),
)


class BottleReading(models.Model):
    temp = models.FloatField()
    weight = models.FloatField()
    time = models.DateTimeField(default=datetime.now)

    def timestamp(self):
        return datetime.timestamp(self.time)


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


class PreviousScore(models.Model):
    calculated = models.DateTimeField(auto_now=True)
    score = models.CharField(max_length=1,
                             choices=SCORE_CHOICES,
                             default='E')
    consumption = models.FloatField(default=0.)
    ideal_consumption = models.FloatField(default=0.)
