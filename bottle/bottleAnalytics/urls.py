from django.urls import path

from .views import interface, api

urlpatterns = [
    # App Interface
    path('', interface.index_view, name='index'),
    path('analytics', interface.analytics_view, name='analytics'),
    path('settings', interface.SettingsUpdate.as_view(), name='settings'),

    path('refresh', interface.refresh_score_view, name='refresh-score'),

    path('delete-readings', interface.delete_readings, name='delete-readings'),
    path('delete-settings', interface.delete_settings, name='delete-settings'),
    path('delete-all', interface.delete_all, name='delete-all'),

    # Bottle API
    path('api/bottleUpdate', api.bottle_update),
]
