from django.db import models

from dance.models import Word


class Collection(models.Model):
    name = models.CharField(max_length=200)
    words = models.ManyToManyField(Word, blank=True)
