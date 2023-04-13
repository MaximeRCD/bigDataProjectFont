from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def dashboard(request):
    context = {'userChart': [28, 40, 36, 52, 38, 60, 55]}
    return render(request, 'dashboard.html', context=context)
