import json
from django.utils import timezone
from django.contrib.sites import requests
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404
import requests
import random
import hashlib
from .models import Quiz, Question, Theme, Response

# Create your views here.


@login_required
def play(request, step):
    if (step == "wait-for-quiz" or step == "quiz" or step == "results") and not 'quiz' in request.session:
        return redirect('play', step="themes")

    if request.method == "POST" and step == "themes":
        themes = []

        for key, value in request.POST.items():
            if key.startswith('theme'):
                themes.append(value)
        themes = themes[:3]

        response = requests.get('http://127.0.0.1:8001/quizz/new_quizz/', json=themes)
        questions = []

        for question in response.json():
            questions.append(question['id'])

        request.session['quiz'] = {"state": "not_started", "questions": questions}
        return redirect('play', step="wait-for-quiz")

    elif request.method == "POST" and step == "wait-for-quiz":
        request.session['quiz']['state'] = "in_progress"
        print(request.session['quiz'])
        return redirect('play', step="quiz")

    elif request.method == 'GET' and step == 'quiz':
        questions_ids = request.session['quiz']['questions']
        questions = Question.objects.filter(id__in=questions_ids).prefetch_related('response_set')

        themes = Theme.objects.filter(question__in=questions).distinct()
        theme_string = ' - '.join([theme.theme for theme in themes])
        return render(request, 'play.html', context={'step': step, 'questions': questions, 'themes': theme_string})

    elif request.method == 'GET' and step == 'results' and 'quiz_hash' in request.session:
        request.session.pop('quiz')
        # 1. Récupérez le quiz en utilisant le quiz_id
        quizs = Quiz.objects.filter(quiz_hash=request.session['quiz_hash'])

        # 2. Récupérez toutes les questions associées au quiz
        questions = Question.objects.filter(quiz__in=quizs)
        print(questions.values_list('id', flat=True))
        # 3. Comptez le nombre total de questions
        total_questions = questions.count()

        # Récupérez les user_answers à partir de la base de données
        user_responses = Quiz.objects.filter(quiz_hash=request.session['quiz_hash']).values_list('response_id', flat=True)

        print(user_responses)
        # 4. Utilisez la liste des réponses de l'utilisateur et récupérez les réponses correctes pour chaque question en une seule requête
        correct_responses = Response.objects.filter(id__in=user_responses, is_true=True).count()

        # 5. Calculez le pourcentage de bonnes réponses
        print(total_questions)
        percentage = int((correct_responses / total_questions) * 100)

        results = {
            'percentage': percentage,
            'numberOfGoodAnswer': correct_responses
        }
        print(results)
        return render(request, 'play.html', context={'step': step, 'results': results, 'quiz_hash': request.session['quiz_hash']})

    elif request.method == "POST" and step == 'create_quizz':
        questions_responses = request.POST.copy()
        questions_responses.pop('csrfmiddlewaretoken', None)
        question_fields = {}
        correction_fields = {}

        for key, value in questions_responses.items():
            if key.startswith('q'):
                question_fields[key] = value
            elif key.startswith('correctionQ'):
                correction_fields[key] = value

        combined_values = str(timezone.now()) + str(request.user.username)
        quiz_hash = hashlib.sha256(combined_values.encode('utf-8')).hexdigest()
        for question, response in question_fields.items():
            quiz = Quiz()
            quiz.user_id = request.user
            quiz.response_id = Response.objects.get(id=response)
            quiz.question_id = Question.objects.get(id=question.replace('q', ''))
            quiz.created_at = timezone.now()
            quiz.quiz_hash = quiz_hash
            quiz.save()
        request.session['quiz']['state'] = "terminated"
        request.session['quiz_hash'] = quiz_hash
        return redirect('play', step="results")

    return render(request, 'play.html', context={'step': step, 'themes': Theme.objects.all()})


def get_questions(request, themes):
    response = '{"questions": [31,32]}'
    return HttpResponse(response)


def fake_model(request):
    response = '{"predicted_label": '+str(random.randint(1, 4))+'}'
    return HttpResponse(response)
