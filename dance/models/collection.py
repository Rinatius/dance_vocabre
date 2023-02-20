from django.db import models

from dance.models.base import BaseDatesModel


class Collection(BaseDatesModel):
    name = models.CharField(max_length=200)
    words = models.ManyToManyField("Word", blank=True)
