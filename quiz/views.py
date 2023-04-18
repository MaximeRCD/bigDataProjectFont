from django.shortcuts import render, redirect
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from play.models import Quiz, Question, Theme

# Create your views here.


@login_required
def quiz_list(request):
    """quizzes = Quiz.objects.filter(user_id=request.user).prefetch_related(
        Prefetch(
            'question_set',
            queryset=Question.objects.select_related('theme').distinct('theme'),
            to_attr='unique_themes'
        )
    )"""
    user = request.user
    quizzes = Quiz.objects.filter(user_id=request.user)

    # Récupérer les thèmes uniques pour chaque quiz
    for quiz in quizzes:
        questions = Question.objects.filter(quiz_id=quiz)
        themes = Theme.objects.filter(question__in=questions)
        theme_set = set(theme.name for theme in themes)
        quiz.unique_themes = ' - '.join(theme_set)

    results = {'percentage': 66.0, 'userAnswers': [1, 3, 2, 4], 'goodAnswers': [1, 1, 2, 3]}
    results['numberOfGoodAnswer'] = sum(ua == ga for ua, ga in zip(results['userAnswers'], results['goodAnswers']))
    results['numberOfBadAnswer'] = sum(ua != ga for ua, ga in zip(results['userAnswers'], results['goodAnswers']))
    return render(request, 'quiz_list.html', context={'quizzes': quizzes, 'results': results})


@login_required
def quiz_attempt(request, quiz_id):
    quiz = Quiz.objects.get(quiz_id=quiz_id)
    if quiz.user_id == request.user:
        quiz = Quiz.objects.select_related('user_id').prefetch_related('question_set', 'question_set__answer_set').get(quiz_id=quiz_id)
        questions = Question.objects.filter(quiz_id=quiz_id)
        themes = Theme.objects.filter(question__in=questions).distinct()
        theme_string = ' - '.join([theme.name for theme in themes])
        return render(request, 'quiz_attempt.html', context={'quiz': quiz, 'themes': theme_string, 'results': {'percentage': 66.0, 'points': 5}})
    else:
        return redirect('quiz_list')
