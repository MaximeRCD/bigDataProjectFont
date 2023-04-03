from django.shortcuts import render

# Create your views here.


def landing(request):
    return render(request, 'landing.html', context={})


def errors(request, code):
    return render(request, 'errors.html', context={'code': code})
