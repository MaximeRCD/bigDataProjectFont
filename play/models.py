from django.db import models

# Create your models here.


class Theme(models.Model):
    name = models.CharField(max_length=50)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Question(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
