from django.db import models

from dance.const import Languages
from dance.models import Learner, Word, Collection


class Stack(models.Model):
    learner = models.ForeignKey(
        Learner, on_delete=models.CASCADE, related_name="stack"
    )
    language = models.CharField(max_length=2, choices=Languages)
    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, related_name="stacks"
    )
    words = models.ManyToManyField(Word, blank=True)
    exclude_words = models.ManyToManyField(Word, blank=True)

    class Meta:
        unique_together = ("learner", "language", "collection")
