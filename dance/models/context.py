from django.db import models

from dance.models.base import BaseDatesModel


class ConText(BaseDatesModel):
    text = models.TextField(
            help_text="Text for the context"
            )

