from django.db import models, transaction

from . import Stack, Collection, Word, Encounter
from .learner import Learner
from ..utils.questiongenerator import make_questions
from ..utils.answergrader import grade
from ..const import (
    QuestionType,
    Languages,
    SelectionType,
    CORRECT_CHOICE,
    INCORRECT_CHOICE,
)
from ..utils.wordselector import select_words


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
        if self.type != QuestionType.KNOWN_SELECTION:
            stack, created = Stack.objects.get_or_create(
                learner=self.learner,
                language=self.test_language,
                collection=self.collection,
            )
            regenerate_stack = (
                created
                or stack.words is None
                or not stack.words.exists()
                or self.regenerate_stack
            )
            if regenerate_stack:
                words = stack.select_new_words(self.stack_size)
            else:
                words = stack.get_words()
        else:
            words = select_words(
                self.learner,
                self.stack_size,
                self.test_language,
                SelectionType.NOT_MARKED,
                self.collection,
            )
            regenerate_stack = False
            stack = False
        self.questions, self.uischema, self.correct_answers = make_questions(
            words, self.type, self.native_language
        )
        with transaction.atomic():
            self.save()
            if regenerate_stack and stack:
                stack.regenerate()

    def process_answers(self, answers=None):
        points = 0
        encounters = []
        correct_words = []
        incorrect_words = []
        if answers is not None:
            self.learner_answers = answers
        for answer in self.correct_answers:
            if answer in self.learner_answers:
                word = Word.objects.get(word=answer)
                # TODO: Possibly remove this request by using word id for optimization.
                correct_answer = self.normalize(self.correct_answers[answer])
                learner_answer = self.normalize(self.learner_answers[answer])
                correct = correct_answer == learner_answer

                if correct:
                    points += 1
                    if self.type:
                        encounter_type = self.type + CORRECT_CHOICE
                    correct_words.append(word.pk)
                else:
                    if self.type:
                        encounter_type = self.type + INCORRECT_CHOICE
                    incorrect_words.append(word.pk)
                encounters.append(
                    Encounter(
                        word=word,
                        learner=self.learner,
                        encounter_type=encounter_type,
                    )
                )
        stack = None
        if self.type != QuestionType.KNOWN_SELECTION:
            stack = Stack.objects.get(
                learner=self.learner,
                language=self.test_language,
                collection=self.collection,
            )
        self.score = round(points / len(self.correct_answers) * 100)
        with transaction.atomic():
            self.save()
            Encounter.objects.bulk_create(encounters)
            if stack:
                stack.exclude_words(correct_words)

    @staticmethod
    def normalize(answer):
        return answer
