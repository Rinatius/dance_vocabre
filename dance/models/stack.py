from django.db import models, transaction

from dance.const import Languages, SelectionType
from dance.models import Learner
from dance.models.base import BaseDatesModel
from dance.utils.wordselector import select_words


class Stack(BaseDatesModel):
    learner = models.ForeignKey(
        Learner, on_delete=models.CASCADE, related_name="stack"
    )
    language = models.CharField(max_length=2, choices=Languages.choices)
    collection = models.ForeignKey(
        "Collection",
        on_delete=models.CASCADE,
        related_name="stacks",
        blank=True,
        null=True,
    )
    words = models.ManyToManyField("Word", blank=True, related_name="stacks")
    excluded_words = models.ManyToManyField(
        "Word", blank=True, related_name="stacks_excluded"
    )

    class Meta:
        unique_together = ("learner", "language", "collection")

    def select_new_words(
        self, amount=10, selection_type=SelectionType.UNKNOWN
    ):
        self.new_words = select_words(
            self.learner,
            amount,
            self.language,
            selection_type,
            self.collection,
        )
        return self.new_words

    def get_words(self):
        if self.words is None or not self.words.exists():
            self.regenerate()
        return self.words.all().exclude(pk__in=self.excluded_words.all())

    def exclude_words(self, words):
        if words:
            words_to_exclude = list(
                self.words.filter(pk__in=words).values_list("id", flat=True)
            )
            self.excluded_words.add(*words_to_exclude)

    def clear_excluded(self):
        self.excluded_words.clear()

    def regenerate(self, amount=10):
        if self.new_words is None:
            self.select_new_words(amount)

        with transaction.atomic():
            self.words.clear()
            self.words.add(*list(self.new_words.values_list("id", flat=True)))
            self.excluded_words.clear()
            self.new_words = None

    def __init__(self, *args, **kwargs):
        self.new_words = None
        super(Stack, self).__init__(*args, **kwargs)
