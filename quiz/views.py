from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def quiz_list(request):
    return render(request, 'quiz_list.html', context={})


@login_required
def quiz_attempt(request, quiz_id):
    # vérifier si le quiz id appartient bien au user
    return render(request, 'quiz_attempt.html', context={})
