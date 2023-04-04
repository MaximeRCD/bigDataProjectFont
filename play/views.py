import json
from django.contrib.sites import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
import requests
import random
# Create your views here.


def play(request, step):
    if step == "wait-for-quiz" and not 'quiz' in request.session:
        return redirect('play', step="themes")
    if request.method == "POST" and step == "themes":
        checked_boxes = [request.POST[f'theme{i}'] for i in range(1, 5) if request.POST.get(f'theme{i}')]
        response = requests.get('http://127.0.0.1:8000/get_questions/'+','.join(checked_boxes)+'/')
        request.session['quiz'] = {"state": "not_started", "id": response.json()}  # in_progress, terminated
        print(request.session['quiz'])
        return redirect('play', step="wait-for-quiz")
    elif request.method == "POST" and step == "wait-for-quiz":
        request.session['quiz']['state'] = "in_progress"  # not_started, terminated
        print(request.session['quiz'])
        return redirect('play', step="quiz")
    return render(request, 'play.html', context={'step': step, 'themes': [{'id': 1, 'name': 'themes1'}, {'id': 2, 'name': 'themes2'}, {'id': 3, 'name': 'themes3'}]})


def get_questions(request, themes):
    response = '{"quiz_id": 1,"questions" : [21,23,43,34]}'
    return HttpResponse(response)


def fake_model(request):
    response = '{"answer": '+str(random.randint(1, 4))+'}'
    return HttpResponse(response)
