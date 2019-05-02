from django.shortcuts import render
from django.http import HttpResponse


def index_view(request):
    return render(request, 'bottleAnalytics/index.html')


def analytics_view(request):
    """Shows the current "health status" to the user of the bottle"""
    # TODO Run the "health algorithm" and respond with current health status.
    return HttpResponse("Your current health status is: ")


def settings_view(request):
    """Show user's settings"""
    return HttpResponse("Settings")
