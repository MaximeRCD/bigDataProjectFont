from django.db import models
from authenticate.models import User
# Create your models here


class Quiz(models.Model):
    user = models.IntegerField(blank=True, null=True)
    questionid = models.IntegerField(db_column='questionId', blank=True, null=True)  # Field name made lowercase.
    iduserresponse = models.IntegerField(db_column='idUserResponse', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False


class Response(models.Model):
    response = models.CharField(max_length=100, blank=True, null=True)
    istrue = models.IntegerField(db_column='isTrue', blank=True, null=True)  # Field name made lowercase.
    idquestion = models.IntegerField(db_column='idQuestion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False


class Theme(models.Model):
    theme = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False


class Type(models.Model):
    type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type'


class Question(models.Model):
    name = models.CharField(max_length=900, blank=True, null=True)
    themeid = models.IntegerField(db_column='themeId', blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
