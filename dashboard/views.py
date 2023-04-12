from django.shortcuts import render

# Create your views here.


def dashboard(request):
    context = {'userChart': [28, 40, 36, 52, 38, 60, 55]}
    return render(request, 'dashboard.html', context=context)
