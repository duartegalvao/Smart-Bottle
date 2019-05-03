from datetime import datetime, timedelta

from django.shortcuts import render

from bottleAnalytics.classify import classify
from bottleAnalytics.models import BottleReading, PreviousScore


def index_view(request):
    p_score = PreviousScore.objects\
        .filter(calculated__gte=datetime.now() - timedelta(hours=1))

    if p_score.exists():
        score = p_score.order_by('-calculated')[0].score
    else:
        readings = BottleReading.objects\
            .filter(time__gte=datetime.now() - timedelta(days=1))\
            .order_by('time')
        score = classify(readings)
        if score != 'E':
            PreviousScore.objects.create(score=score)

    return render(request, 'bottleAnalytics/index.html', context={
        'score': score,
    })


def analytics_view(request):
    """Shows the current "health status" to the user of the bottle"""
    p_scores = PreviousScore.objects.all().order_by('-calculated')
    return render(request, 'bottleAnalytics/analytics.html', context={
        'scores': p_scores,
    })


def settings_view(request):
    """Show user's settings and allow them to edit"""
    return render(request, 'bottleAnalytics/settings.html')
