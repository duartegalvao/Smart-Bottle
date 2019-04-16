from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("This is the bottle index.")

# Comes from the bottle
def bottleUpdate(request):
    # TODO Update BottleStats with the readings received in the request
    return HttpResponse("BottleStats has been updated")

# Comes from the user
def getHealthStatus(request):
    # TODO Run the "health algorithm" and respond with current health status.
    return HttpResponse("Your current health status is: ")
