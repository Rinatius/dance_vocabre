from django.db import models

from .base import BaseDatesModel
from .system import System


class Learner(BaseDatesModel):
    external_id = models.CharField(max_length=200)
    system = models.ForeignKey(
            System,
            on_delete=models.CASCADE,
            related_name="Learners",
            help_text="System which Learner belongs to"
            )

