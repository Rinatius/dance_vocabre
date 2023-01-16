from django.db import models

from .learner import Learner
from ..utils.questiongenerator import generate_questions
from ..utils.answergrader import grade
from ..const import AnswerSheetType


class AnswerSheet(models.Model):

    type = models.CharField(max_length=2, choices=AnswerSheetType.choices)

    questions = models.TextField(
        blank=True,
        null=True,
        help_text="Questions in JSON Schema format",
    )

    correct_answers = models.TextField(
        blank=True,
        null=True,
        help_text=(
            "Correct answers in JSON format matching schema in Questions"
        ),
    )

    learner_answers = models.TextField(
        blank=True,
        null=True,
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

    def generate_questions(self):
        self.questions, self.correct_answers = generate_questions(
            self.type, self.learner, amount=10
        )

    def grade_answers(self):
        self.score = grade(
            self.questions,
            self.correct_answers,
            self.learner_answers,
        )

    def generate_encounters(self):
        pass
