from django.db import models, transaction

from dance.const import Languages, SelectionType
from dance.models import Learner, Word, Collection
from dance.utils.wordselector import select_words


class Stack(models.Model):
    learner = models.ForeignKey(
        Learner, on_delete=models.CASCADE, related_name="stack"
    )
    language = models.CharField(max_length=2, choices=Languages)
    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, related_name="stacks"
    )
    words = models.ManyToManyField(Word, blank=True)
    excluded_words = models.ManyToManyField(Word, blank=True)

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
        self.excluded_words.add(words.filter(pk__in=self.words.all))

    def clear_excluded(self):
        self.excluded_words.clear()

    def regenerate(self, amount=10):
        if self.new_words is None:
            self.select_new_words(amount)
        with transaction.atomic():
            self.words.clear()
            self.words.add(self.new_words)
            self.excluded_words.clear()
            self.new_words = None

    def __init__(self, *args, **kwargs):
        self.new_words = None
        super(Stack, self).__init__(*args, *kwargs)
