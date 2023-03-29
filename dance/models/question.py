from django.db import models

from .base import BaseDatesModel
from .context import ConText
from .word import Word


class Question(BaseDatesModel):
    schema = models.TextField(
            help_text="Question JSON Schema"
            )
    context = models.ForeignKey(
            ConText,
            null=True,
            on_delete=models.CASCADE,
            related_name="questions",
            help_text="Context for the questions"
            )
    text = models.TextField(
            help_text="Text for the question"
            )
    correct_response = models.TextField(
            help_text="Correct response JSON"
            )
    words = models.ManyToManyField(
            Word,
            related_name="questions",
            help_text="Words tested in the question"
            )
    def is_correct(self, response):
        pass

