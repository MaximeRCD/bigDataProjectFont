from django.contrib import admin
from .models import Question, Theme, Quiz, Response, Type

# Register your models here.

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Theme)
admin.site.register(Response)
admin.site.register(Type)
