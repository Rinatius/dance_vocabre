from django.contrib import admin

from .models import Word, Learner, System, Encounter
from .models.answersheet import AnswerSheet


class WordAdmin(admin.ModelAdmin):
    list_display = ("word", "language", "order")


admin.site.register(Word, WordAdmin)
admin.site.register(AnswerSheet)
admin.site.register(Learner)
admin.site.register(System)
admin.site.register(Encounter)
