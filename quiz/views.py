from django.shortcuts import render, redirect
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from play.models import Quiz, Question, Theme, Response
from collections import defaultdict

# Create your views here.


@login_required
def quiz_list(request):
    quizzes = Quiz.objects.filter(user_id_id=request.user.id)
    grouped_quizzes = defaultdict(list)
    for quiz in quizzes:
        grouped_quizzes[quiz.quiz_hash].append(quiz)

    quiz_info = {}
    for quiz_hash, quiz_list in grouped_quizzes.items():
        total_questions = len(quiz_list)
        correct_answers = sum(1 for quiz in quiz_list if quiz.response_id.is_true)
        incorrect_answers = total_questions - correct_answers
        success_rate = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0

        themes = '-'.join(set(quiz.question_id.theme_id.theme for quiz in quiz_list))

        quiz_info[quiz_hash] = {
            'total_questions': total_questions,
            'numberOfGoodAnswer': correct_answers,
            'numberOfBadAnswer': incorrect_answers,
            'percentage': success_rate,
            'themes': themes,
            'quiz_date': quiz_list[0].created_at if quiz_list else None
        }
    return render(request, 'quiz_list.html', context={'quizzes': quizzes, 'quiz_info': quiz_info})


@login_required
def quiz_attempt(request, quiz_hash):
    quizzes = Quiz.objects.filter(quiz_hash=quiz_hash, user_id_id=request.user.id).select_related('question_id', 'response_id')
    if quizzes.exists():
        # Calculer les résultats
        total_questions = quizzes.count()
        correct_answers = sum(1 for quiz in quizzes if quiz.response_id.is_true)
        points = correct_answers  # Assumant que chaque bonne réponse vaut 1 point
        percentage = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0

        results = {
            'points': points,
            'percentage': percentage,
        }

        # Récupérer les thèmes
        themes = '-'.join(set(quiz.question_id.theme_id.theme for quiz in quizzes))

        # Récupérer les questions et leurs réponses associées
        questions = []
        for quiz in quizzes:
            question = quiz.question_id
            user_response = quiz.response_id
            all_responses = Response.objects.filter(id_question_id=question.id)
            questions.append((question, user_response, all_responses))
        return render(request, 'quiz_attempt.html', context={'themes': themes, 'results': results, 'questions': questions})
    else:
        return redirect('quiz_list')
