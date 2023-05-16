from django.shortcuts import render
from authenticate.models import User
from play.models import Quiz, Question

# Create your views here.


def landing(request):
    users_number = User.objects.all().count()
    quiz_number = Quiz.objects.values('quiz_hash').distinct().count()
    questions_number = Question.objects.all().count()
    return render(request, 'landing.html', context={'users_number': users_number, 'quiz_number': quiz_number, 'questions_number': questions_number})
