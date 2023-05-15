import json
from django.contrib.sites import requests
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404
import requests
import random
from .models import Quiz, Question, Theme, Response

# Create your views here.


@login_required
def play(request, step):
    if (step == "wait-for-quiz" or step == "quiz" or step == "results") and not 'quiz' in request.session:
        return redirect('play', step="themes")

    if request.method == "POST" and step == "themes":
        checked_boxes = [request.POST[f'theme{i}'] for i in range(1, 5) if request.POST.get(f'theme{i}')]
        response = requests.get('http://127.0.0.1:8000/get_questions/'+','.join(checked_boxes)+'/')
        request.session['quiz'] = {"state": "not_started", "questions": response.json()['questions']}
        return redirect('play', step="wait-for-quiz")

    elif request.method == "POST" and step == "wait-for-quiz":
        request.session['quiz']['state'] = "in_progress"
        print(request.session['quiz'])
        return redirect('play', step="quiz")

    elif request.method == 'GET' and step == 'quiz':
        print(request.session['quiz'])
        questions_ids = request.session['quiz']['questions']
        questions = Question.objects.filter(id__in=questions_ids).prefetch_related('response_set')

        themes = Theme.objects.filter(question__in=questions).distinct()
        theme_string = ' - '.join([theme.theme for theme in themes])
        return render(request, 'play.html', context={'step': step, 'questions': questions, 'themes': theme_string})

    elif request.method == 'GET' and step == 'results':
        request.session['quiz']['state'] = "terminated"
        quiz_hash = 'f6d233e2621878b3a88d22ec24de73f6e83aa6cc4cfa49a600430dc6edeeef0f'
        # 1. Récupérez le quiz en utilisant le quiz_id
        quizs = Quiz.objects.filter(quiz_hash=quiz_hash)

        # 2. Récupérez toutes les questions associées au quiz
        questions = Question.objects.filter(quiz__in=quizs)
        print(questions.values_list('id', flat=True))
        # 3. Comptez le nombre total de questions
        total_questions = questions.count()

        # Récupérez les user_answers à partir de la base de données
        user_responses = Quiz.objects.filter(quiz_hash=quiz_hash).values_list('response_id', flat=True)

        print(user_responses)
        # 4. Utilisez la liste des réponses de l'utilisateur et récupérez les réponses correctes pour chaque question en une seule requête
        correct_responses = Response.objects.filter(id__in=user_responses, is_true=True).count()

        # 5. Calculez le pourcentage de bonnes réponses
        print(total_questions)
        percentage = (correct_responses / total_questions) * 100

        results = {
            'percentage': percentage,
            'numberOfGoodAnswer': correct_responses
        }
        print(results)
        return render(request, 'play.html', context={'step': step, 'results': results})

    elif request.method == 'POST' and step == 'results':
        request.session.pop('quiz')
        return redirect('quiz')

    elif request.method == "POST" and step == 'create_quizz':
        print("post : ", request.POST)
        return HttpResponse({"isCreated": "True"})

    return render(request, 'play.html', context={'step': step, 'themes': [{'id': 1, 'name': 'themes1'}, {'id': 2, 'name': 'themes2'}, {'id': 3, 'name': 'themes3'}]})


def get_questions(request, themes):
    response = '{"questions": [1,2,3,4]}'
    return HttpResponse(response)


def fake_model(request):
    response = '{"predicted_label": '+str(random.randint(1, 4))+'}'
    return HttpResponse(response)
