from django.db import models
from authenticate.models import User
# Create your models here


class Type(models.Model):
    type = models.CharField(max_length=100, null=True)


class Theme(models.Model):
    theme = models.CharField(max_length=100, null=True)


class Question(models.Model):
    name = models.CharField(max_length=900, null=True)
    theme_id = models.ForeignKey(Theme, db_column='themeId', on_delete=models.DO_NOTHING)
    type_id = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(db_column='createdAt', null=True)


class Response(models.Model):
    response = models.CharField(max_length=100, null=True)
    is_true = models.BooleanField(db_column='isTrue', null=True)  # Field name made lowercase.
    id_question = models.ForeignKey(Question, db_column='idQuestion', on_delete=models.DO_NOTHING)


class Quiz(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question_id = models.ForeignKey(Question, db_column='questionId', on_delete=models.DO_NOTHING)
    response_id = models.ForeignKey(Response, db_column='idUserResponse', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(db_column='CreatedAt', null=True)
