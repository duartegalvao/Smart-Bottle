from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('bottleUpdate', views.bottleUpdate, name='bottleUpdate'),
        path('getHealthStatus', views.getHealthStatus, name='getHealthStatus')
            ]
