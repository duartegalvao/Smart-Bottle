from django.urls import path

from .views import interface, api

urlpatterns = [
    # App Interface
    path('', interface.index, name='index'),
    path('getHealthStatus', interface.get_health_status, name='getHealthStatus'),

    # Bottle API
    path('api/bottleUpdate', api.bottle_update, name='bottleUpdate'),
]
