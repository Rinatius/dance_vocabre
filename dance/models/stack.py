from django.db import models, transaction

from dance.const import Languages, SelectionType
from dance.models import Learner
from dance.utils.wordselector import select_words


class Stack(models.Model):
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
        print("----------------NEW WORDS----------------")
        self.new_words = select_words(
            self.learner,
            amount,
            self.language,
            selection_type,
            self.collection,
        )
        print("----------------NEW WORDS DONE----------------")
        print(self.new_words)
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
        print("-----------NEW WORDS INSIDE REGENERATE----------------")

        print(self.new_words)
        if self.new_words is None:
            self.select_new_words(amount)

        with transaction.atomic():
            self.words.clear()
            print("-------------WORDS CLEARED--------------")
            print(list(self.new_words.values_list("id", flat=True)))
            self.words.add(*list(self.new_words.values_list("id", flat=True)))
            print("-----------WORDS ADDED----------------")

            self.excluded_words.clear()
            self.new_words = None
        print("-----------REGENERATE DONE----------------")

    def __init__(self, *args, **kwargs):
        self.new_words = None
        super(Stack, self).__init__(*args, **kwargs)
