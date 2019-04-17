from django.db import models
import datetime

# Create your models here.

# class Bottle(models.Model):
#     def newBottleReading(temp, weight):
        


class BottleReading(models.Model):
    temp = models.IntegerField(default=150)
    weight = models.IntegerField(default=150)

#    def __init__(self, temp, weight):
#        self.temp = temp
#        self.weight = weight
#        self.time = datetime.now().time()

# class BottleAnalytics(models.Model):
# #     aBottleReading = BottleReadin
# #     allBottleReadings = BottleReading.objects.all()
#     bottleReading = bottleReading()
#     bottleReadings = bottleReading.objects
#     def getBottleReadings(self):
#         print (bottleReadings)
# 

# class BottleStats(models.Model):


