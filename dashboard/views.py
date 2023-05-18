import json

import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from play.models import Theme

# Create your views here.


@login_required
def dashboard(request):
    theme_plus_choisi = requests.get('https://api-k3dvzrn44a-od.a.run.app/statisques_personnel/theme_plus_choisi?user_id='+str(request.user.id))
    theme_reussi = requests.get('https://api-k3dvzrn44a-od.a.run.app/statisques_personnel/theme_reussi?user_id=' + str(request.user.id))
    theme_moins_reussi = requests.get('https://api-k3dvzrn44a-od.a.run.app/statisques_personnel/theme_moins_reussi?user_id=' + str(request.user.id))

    context = {'userChart': [28, 40, 36, 52, 38, 60, 55], 'menber_since': account_age_view(request)}
    try:
        if len(theme_plus_choisi.json()) > 0:
            context['most_choosen_theme'] = Theme.objects.get(id=theme_plus_choisi.json()[0]['themeId']).theme
        else:
            context['most_choosen_theme'] = '...'
    except json.JSONDecodeError as e:
        context['most_choosen_theme'] = '...'

    try:
        context['successful_theme'] = Theme.objects.get(id=theme_reussi.json()[0]['themeId']).theme
    except json.JSONDecodeError as e:
        context['successful_theme'] = '...'

    try:
        context['unsuccessful_theme'] = Theme.objects.get(id=theme_moins_reussi.json()[0]['themeId']).theme
    except json.JSONDecodeError as e:
        context['unsuccessful_theme'] = '...'

    return render(request, 'dashboard.html', context=context)


def account_age_view(request):
    user = request.user
    delta = (timezone.now() - user.date_joined).days
    if delta < 30:
        return f"{delta} day" + ("s" if delta > 1 else "")
    elif delta < 365:
        return f"{delta // 30} month" + ("s" if delta // 30 > 1 else "")
    else:
        return f"{delta // 365} year" + ("s" if delta // 365 > 1 else "")
