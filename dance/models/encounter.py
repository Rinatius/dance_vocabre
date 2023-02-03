from django.db import models

from .learner import Learner
from .word import Word
from ..const import EncounterType


class Encounter(models.Model):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="encounters",
        help_text="Word encountered by Learner",
    )
    learner = models.ForeignKey(
        Learner,
        on_delete=models.CASCADE,
        related_name="encounters",
        help_text="Learner who encountered the Word",
    )
    encounter_type = models.CharField(
        max_length=4, choices=EncounterType.choices
    )

    def __str__(self):
        return f"{self.word} - {self.learner} - {self.encounter_type}"
