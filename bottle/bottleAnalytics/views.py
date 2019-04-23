from django.shortcuts import render
from django.http import HttpResponse
from bottleAnalytics.models import BottleReading
from django.views.decorators.csrf import csrf_exempt

# TEST bottleUpdate
# curl --data "temp=10&weight=11" localhost:8000/bottleAnalytics/bottleUpdate

def index(request):
    return HttpResponse("This is the bottle index.")

# Receives parameters from the bottle
@csrf_exempt
def bottleUpdate(request):
    newBottleReading = BottleReading()
    newBottleReading.temp = request.POST.get('temp')
    newBottleReading.weight = request.POST.get('weight')
    newBottleReading.save()
    return HttpResponse("BottleStats has been updated")

# Shows the current "health status" to the user of the bottle
def getHealthStatus(request):
    # TODO Run the "health algorithm" and respond with current health status.
    return HttpResponse("Your current health status is: ")
