from django.shortcuts import render
from django.http import HttpResponse
from bottleAnalytics.models import BottleReading

def index(request):
    return HttpResponse("This is the bottle index.")

# Comes from the bottle
def bottleUpdate(request):
    # TODO Update BottleStats with the readings received in the request
    newBottleReading = BottleReading()
    newBottleReading.temp = 77
    newBottleReading.weight = 78
    newBottleReading.save()
    return HttpResponse("BottleStats has been updated")

# Comes from the user
def getHealthStatus(request):
    # TODO Run the "health algorithm" and respond with current health status.
    return HttpResponse("Your current health status is: ")
