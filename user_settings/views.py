from django.shortcuts import render

# Create your views here.


def user_settings(request):
    return render(request, 'user_settings.html', context={})