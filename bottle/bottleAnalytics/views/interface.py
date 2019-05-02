from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("This is the bottle index.")


# Shows the current "health status" to the user of the bottle
def get_health_status(request):
    # TODO Run the "health algorithm" and respond with current health status.
    return HttpResponse("Your current health status is: ")
