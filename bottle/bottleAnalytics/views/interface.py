from datetime import datetime, timedelta

from django.contrib import messages
from django.forms import modelform_factory, SelectDateWidget
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from bottleAnalytics.classify import classify, smooth_readings
from bottleAnalytics.models import BottleReading, PreviousScore, UserSettings


def index_view(request):
    p_score = PreviousScore.objects\
        .filter(calculated__gte=datetime.now() - timedelta(hours=1))

    if p_score.exists():
        score = p_score.order_by('-calculated')[0].score
    else:
        score = create_score()

    if UserSettings.get_solo().birth_date is None:
        messages.warning(request, "Don't forget to define your personal settings for more accurate results!")

    return render(request, 'bottleAnalytics/index.html', context={
        'score': score,
    })


def analytics_view(request):
    """Shows the current "health status" to the user of the bottle"""
    readings = BottleReading.objects\
        .filter(time__gte=datetime.now() - timedelta(days=1)) \
        .order_by('time')
    readings_s = smooth_readings(readings)
    p_scores = PreviousScore.objects.all().order_by('-calculated')

    return render(request, 'bottleAnalytics/analytics.html', context={
        'readings': readings,
        'readings_s': readings_s,
        'scores': p_scores,
    })


class SettingsUpdate(UpdateView):
    model = UserSettings
    get_object = model.get_solo
    success_url = reverse_lazy('refresh-score')
    form_class = modelform_factory(model,
                                   exclude=[],
                                   widgets={
                                        'birth_date': SelectDateWidget(years=range(1900, datetime.now().year))
                                    })


def refresh_score_view(request):
    create_score()
    return redirect('index')


def delete_readings(request):
    if request.method == 'POST':
        BottleReading.objects.all().delete()
        PreviousScore.objects.all().delete()
        return redirect('index')
    else:
        return render(request, 'bottleAnalytics/delete.html', context={
            'what_short': "Readings",
            'what_long': "all of your readings and scores",
        })


def delete_settings(request):
    if request.method == 'POST':
        UserSettings.get_solo().delete()
        return redirect('index')
    else:
        return render(request, 'bottleAnalytics/delete.html', context={
            'what_short': "Settings",
            'what_long': "all of your personal settings",
        })


def delete_all(request):
    if request.method == 'POST':
        BottleReading.objects.all().delete()
        PreviousScore.objects.all().delete()
        UserSettings.get_solo().delete()
        return redirect('index')
    else:
        return render(request, 'bottleAnalytics/delete.html', context={
            'what_short': "All Data",
            'what_long': "all application data",
        })


# Aux fucntions
def create_score():
    readings = BottleReading.objects \
        .filter(time__gte=datetime.now() - timedelta(days=1)) \
        .order_by('time')
    score, consumption, ideal_consumption = classify(readings, UserSettings.get_solo())
    if score != 'E':
        PreviousScore.objects.create(score=score,
                                     consumption=consumption,
                                     ideal_consumption=ideal_consumption)
    return score
