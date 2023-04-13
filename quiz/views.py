from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def quiz(request):
    return render(request, 'quiz.html', context={})
