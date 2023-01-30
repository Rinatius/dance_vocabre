from django.db import models

from . import Stack, Collection, Word
from .learner import Learner
from ..utils.questiongenerator import make_questions
from ..utils.answergrader import grade
from ..const import QuestionType, Languages


class AnswerSheet(models.Model):

    type = models.CharField(max_length=2, choices=QuestionType.choices)

    questions = models.JSONField(
        default=dict,
        help_text="Questions in JSON Schema format",
    )

    uischema = models.JSONField(
        default=dict,
        help_text="UI schema for Questions in JSON Schema React Form format",
    )

    correct_answers = models.JSONField(
        default=dict,
        help_text=(
            "Correct answers in JSON format matching schema in Questions"
        ),
    )

    learner_answers = models.JSONField(
        default=dict,
        help_text=(
            "Answers by Learner in JSON format matching schema in Questions"
        ),
    )

    learner = models.ForeignKey(
        Learner,
        on_delete=models.CASCADE,
        related_name="responses",
        help_text="Responding Learner",
    )

    score = models.IntegerField(
        null=True, help_text="Percentage of correct responses"
    )

    test_language = models.CharField(
        max_length=2, choices=Languages.choices, default=Languages.ENGLISH
    )

    native_language = models.CharField(
        max_length=2, choices=Languages.choices, default=Languages.ENGLISH
    )

    collection = models.ForeignKey(
        Collection,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=(
            "Selection of words that limits question generation for an"
            " Answersheet instance. If null, all words are considered for this"
            " particular user and language. Collection also influences which"
            " Stack is used."
        ),
    )
    stack_size = models.IntegerField(blank=True, null=True)
    regenerate_stack = models.BooleanField(
        default=False,
        help_text=(
            "Flag indicating that Stack Answrsheet is using to make questions"
            " should be regenerated"
        ),
    )

    def grade_answers(self):
        self.score = grade(
            self.questions,
            self.correct_answers,
            self.learner_answers,
        )

    def generate_encounters(self):
        pass

    def generate(self):
        self.type,
        self.learner,
        self.test_language,
        self.native_language,
        stack_words =
        if self.regenerate_stack:
            stack
        words = Word.objects.all()
        self.questions, self.uischema, self.answers = make_questions(
            words, self.type, self.native_language
        )
