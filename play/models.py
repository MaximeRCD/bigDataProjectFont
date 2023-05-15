import hashlib

from django.db import models
from authenticate.models import User
# Create your models here


class Type(models.Model):
    type = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'type'


class Theme(models.Model):
    theme = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'theme'


class Question(models.Model):
    name = models.CharField(max_length=900, null=True)
    theme_id = models.ForeignKey(Theme, db_column='themeId', on_delete=models.DO_NOTHING)
    type_id = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(db_column='createdAt', null=True)

    class Meta:
        db_table = 'question'


class Response(models.Model):
    response = models.CharField(max_length=100, null=True)
    is_true = models.BooleanField(db_column='isTrue', null=True)  # Field name made lowercase.
    id_question = models.ForeignKey(Question, db_column='idQuestion', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'response'


class Quiz(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question_id = models.ForeignKey(Question, db_column='questionId', on_delete=models.DO_NOTHING)
    response_id = models.ForeignKey(Response, db_column='idUserResponse', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(db_column='CreatedAt', null=True)
    quiz_hash = models.CharField(max_length=64, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.quiz_hash:
            # Concaténez l'ID de l'utilisateur et la date de création sous forme de chaîne de caractères
            combined_values = str(self.user_id) + str(self.created_at)

            # Créez un hash SHA-256 de la chaîne combinée
            hash_object = hashlib.sha256(combined_values.encode('utf-8'))
            hash_string = hash_object.hexdigest()

            # Définissez la valeur du champ hash_value
            self.hash_value = hash_string

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'quizz'
