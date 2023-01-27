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
        max_length=2, choices=EncounterType.choices
    )
