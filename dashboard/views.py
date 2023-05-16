import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.


@login_required
def dashboard(request):
    response = requests.get('http://127.0.0.1:8001/stat_perso/theme_plus_choisi', json=request.user.id)
    print(response.json())
    context = {'userChart': [28, 40, 36, 52, 38, 60, 55], 'menber_since': account_age_view(request)}
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
