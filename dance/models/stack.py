from django.db import models

from dance.models import Learner, Word


class Stack(models.Model):
    learner = models.ForeignKey(
        Learner, on_delete=models.CASCADE, related_name="stack"
    )
    words = models.ManyToManyField(Word, blank=True)
