from django.db import models

from ..const import Languages


class Word(models.Model):
    word = models.CharField(max_length=200)
    order = models.IntegerField()
    translations = models.ManyToManyField(
        "self",
        symmetrical=True,
        blank=True,
        help_text="Translations of the word into other languages and synonyms",
    )
    language = models.CharField(
        max_length=2, choices=Languages.choices, default=Languages.ENGLISH
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.word} - {self.language}"
