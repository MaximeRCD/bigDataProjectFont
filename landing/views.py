import requests
from django.shortcuts import render
from authenticate.models import User
from play.models import Quiz, Question, Theme

# Create your views here.


def landing(request):
    users_number = User.objects.all().count()
    quiz_number = Quiz.objects.values('quiz_hash').distinct().count()
    questions_number = Question.objects.all().count()
    response = requests.get('https://api-k3dvzrn44a-od.a.run.app/statisques_general/top5themes')
    top_themes = []
    for i, theme in enumerate(response.json()):
        if i < 2:
            top_themes.append({'theme': Theme.objects.get(id=theme['themeId']).theme, 'number': theme['evaluation']})

    return render(request, 'landing.html', context={'users_number': users_number, 'quiz_number': quiz_number, 'questions_number': questions_number, 'top_themes': top_themes})
