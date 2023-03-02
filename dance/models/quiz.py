from django.db import models

from .base import BaseDatesModel
from .question import Question


class Quiz(BaseDatesModel):
    questions = models.ManyToManyField(
        Question, related_name="questions", help_text="Quiz questions"
    )
