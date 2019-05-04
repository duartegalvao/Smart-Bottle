from django.urls import path

from .views import interface, api

urlpatterns = [
    # App Interface
    path('', interface.index_view, name='index'),
    path('analytics', interface.analytics_view, name='analytics'),
    path('settings', interface.settings_view, name='settings'),

    path('refresh', interface.refresh_score_view, name='refresh-score'),

    # Bottle API
    path('api/bottleUpdate', api.bottle_update),
]
