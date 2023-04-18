from django.db import models
from authenticate.models import User
# Create your models here


class Quiz(models.Model):
    quiz_id = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    quiz_date = models.DateTimeField(auto_now_add=True)


class Theme(models.Model):
    name = models.CharField(max_length=50)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Question(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    user_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.text
