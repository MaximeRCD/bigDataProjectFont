import json
from datetime import datetime, timedelta

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
    evolution = requests.get('https://api-k3dvzrn44a-od.a.run.app/statisques_personnel/evolution?user_id=' + str(request.user.id))
    colors = ['#754ffe', '#38a169', '#dc2626', '#0ea5e9', '#f59e0b']
    colors_label = ['primary', 'success', 'danger', 'info', 'warning']
    context = {'userChart': [28, 40, 36, 52, 38, 60, 55], 'menber_since': account_age_view(request)}
    try:
        if len(theme_plus_choisi.json()) > 0:
            # Calculate total evaluation
            total_evaluation = sum([int(item['evaluation']) for item in theme_plus_choisi.json()])
            # Calculate percentage for each theme
            context['percentage_per_theme'] = [int((item['evaluation'] / total_evaluation) * 100) for item in theme_plus_choisi.json()]
            # Extract theme ids
            context['themes'] = [Theme.objects.get(id=item['themeId']).theme for item in theme_plus_choisi.json()]
            #Colors
            context['colors'] = colors[:len(context['themes'])]
            context['legend'] = zip(colors_label[:len(context['themes'])], context['themes'], context['percentage_per_theme'])
            context['most_choosen_theme'] = Theme.objects.get(id=theme_plus_choisi.json()[0]['themeId']).theme
        else:
            context['most_choosen_theme'] = '...'
    except json.JSONDecodeError as e:
        context['most_choosen_theme'] = '...'
    except IndexError as e:
        context['successful_theme'] = '...'

    try:
        if len(theme_reussi.json()) > 0:
            context['successful_theme'] = Theme.objects.get(id=theme_reussi.json()[-1]['themeId']).theme
        else:
            context['successful_theme'] = '...'
    except json.JSONDecodeError as e:
        context['successful_theme'] = '...'
    except IndexError as e:
        context['successful_theme'] = '...'

    try:
        if len(theme_moins_reussi.json()) > 0:
            context['unsuccessful_theme'] = Theme.objects.get(id=theme_moins_reussi.json()[0]['themeId']).theme
        else:
            context['unsuccessful_theme'] = '...'
    except json.JSONDecodeError as e:
        context['unsuccessful_theme'] = '...'
    except IndexError as e:
        context['successful_theme'] = '...'

    try:
        evolution_data = evolution.json()
        if len(evolution_data) > 0:
            # Convert "CreatedAt" strings to date objects
            for item in evolution_data:
                item['CreatedAt'] = datetime.strptime(item['CreatedAt'], '%Y-%m-%d').date()

            # Today's date
            today = datetime.today().date()

            # Number of quizzes created each day
            quizzes_per_day = {}
            for item in evolution_data:
                if item['CreatedAt'] not in quizzes_per_day:
                    quizzes_per_day[item['CreatedAt']] = 0
                quizzes_per_day[item['CreatedAt']] += item['quizz']
            # Sort quizzes_per_day by date
            quizzes_per_day_sorted = dict(sorted(quizzes_per_day.items()))

            # Create a list of number of quizzes for each day
            context['quizzes_list'] = list(quizzes_per_day_sorted.values()) if len(list(quizzes_per_day_sorted.values())) > 1 else [0] + list(quizzes_per_day_sorted.values())
            # Number of quizzes created in the last 7 days and the last 30 days and today
            context['quizzes_last_7_days'] = sum(quizzes for date, quizzes in quizzes_per_day.items() if today - date <= timedelta(days=7))
            context['quizzes_last_30_days'] = sum(quizzes for date, quizzes in quizzes_per_day.items() if today - date <= timedelta(days=30))
            context['quizzes_today'] = quizzes_per_day.get(today, 0)
            dates_list = list(quizzes_per_day_sorted.keys())
            context['first_date'] = dates_list[0]
            context['last_date'] = dates_list[-1]
    except json.JSONDecodeError as e:
        context['quizzes_list'] = []
        context['quizzes_last_7_days'] = '...'
        context['quizzes_last_30_days'] = '...'
        context['quizzes_today'] = '...'
        context['first_date'] = '...'
        context['last_date'] = '...'
    except IndexError as e:
        context['quizzes_list'] = []
        context['quizzes_last_7_days'] = '...'
        context['quizzes_last_30_days'] = '...'
        context['quizzes_today'] = '...'
        context['first_date'] = '...'
        context['last_date'] = '...'
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
