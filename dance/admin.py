from django.contrib import admin

from .models import Word, Learner, System
from .models.answersheet import AnswerSheet

admin.site.register(Word)
admin.site.register(AnswerSheet)
admin.site.register(Learner)
admin.site.register(System)
