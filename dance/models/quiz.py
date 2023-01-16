from django.db import models
from .question import Question


class Quiz(models.Model):
    questions = models.ManyToManyField(
            Question,
            related_name="questions",
            help_text="Quiz questions"
            )
