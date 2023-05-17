import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from play.models import Theme

# Create your views here.


@login_required
def dashboard(request):
    theme_plus_choisi = requests.get('http://127.0.0.1:8001/statisques_personnel/theme_plus_choisi?user_id='+str(request.user.id))
    print(theme_plus_choisi.json())
    theme_reussi = requests.get('http://127.0.0.1:8001/statisques_personnel/theme_reussi?user_id=' + str(request.user.id))
    print(theme_reussi.json())
    theme_moins_reussi = requests.get('http://127.0.0.1:8001/statisques_personnel/theme_moins_reussi?user_id=' + str(request.user.id))
    print(theme_moins_reussi.json())

    context = {'userChart': [28, 40, 36, 52, 38, 60, 55], 'menber_since': account_age_view(request)}
    if len(theme_plus_choisi.json()) > 0:
        context['most_choosen_theme'] = Theme.objects.get(id=theme_plus_choisi.json()[0]['themeId']).theme
    else:
        context['most_choosen_theme'] = '...'

    if len(theme_reussi.json()) > 0:
        context['successful_theme'] = Theme.objects.get(id=theme_reussi.json()[0]['themeId']).theme
    else:
        context['successful_theme'] = '...'

    if len(theme_moins_reussi.json()) > 0:
        context['unsuccessful_theme'] = Theme.objects.get(id=theme_moins_reussi.json()[0]['themeId']).theme
    else:
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
