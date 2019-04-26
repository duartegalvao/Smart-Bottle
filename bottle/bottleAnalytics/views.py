from django.shortcuts import render
from django.http import HttpResponse
from bottleAnalytics.models import BottleReading
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# TEST bottleUpdate
# curl --data "temp=10&weight=11" localhost:8000/bottleAnalytics/bottleUpdate

@method_decorator(csrf_exempt)
def index(request):
    return HttpResponse("This is the bottle index.")

# Receives parameters from the bottle
@method_decorator(csrf_exempt)
def bottleUpdate(request):
    print("Inside bottleUpdate")
    newBottleReading = BottleReading()
    newBottleReading.temp = request.POST.get('temp')
    newBottleReading.weight = request.POST.get('weight')
    newBottleReading.save()
    print("Updated with temp %s and weight %s", newBottleReading.temp, newBottleReading.weight)
    return HttpResponse("BottleStats has been updated")

# Shows the current "health status" to the user of the bottle
@method_decorator(csrf_exempt)
def getHealthStatus(request):
    # TODO Run the "health algorithm" and respond with current health status.
    return HttpResponse("Your current health status is: ")
