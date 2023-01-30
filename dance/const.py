from enum import Enum
from django.db import models
from django.utils.translation import gettext_lazy as _

CORRECT_CHOICE = "C"
INCORRECT_CHOICE = "I"


class QuestionType(models.TextChoices):
    MULTI_CHOICE_QUIZ = "MQ", _("Multiple choice quiz")
    MULTI_CHOICE_IN_NATIVE_QUIZ = "NQ", _(
        "Multiple choice quiz with choices in native language"
    )
    SPELL_QUIZ = "SQ", _("Spelling quiz")
    FAMILIAR_SELECTION = "SF", _("Familiar selection")
    KNOWN_SELECTION = "SK", _("Known selection")


class EncounterType(models.TextChoices):
    # PURE_CONTEXT = "PC", _("Pure context")
    # QUIZ_CONTEXT = "QC", _("Quiz context")
    # QUIZ_TARGET = "QT", _("Quiz target")
    # QUIZ_OPTIONS = "QO", _("Quiz options")
    # QUIZ_INCORRECT = "QI", _("Quiz incorrect answer")
    MULTI_CHOICE_QUIZ_CORRECT = (
        QuestionType.MULTI_CHOICE_QUIZ + CORRECT_CHOICE,
        _("Correct answer to multiple choice question"),
    )
    MULTI_CHOICE_QUIZ_INCORRECT = (
        QuestionType.MULTI_CHOICE_QUIZ + INCORRECT_CHOICE,
        _("Incorrect answer to multiple choice question"),
    )
    MULTI_CHOICE_IN_NATIVE_QUIZ = (
        QuestionType.MULTI_CHOICE_IN_NATIVE_QUIZ + CORRECT_CHOICE,
        _(
            "Correct answer to multiple choice quiz with choices in native"
            " language"
        ),
    )
    MULTI_CHOICE_IN_NATIVE_QUIZ_INCORRECT = (
        QuestionType.MULTI_CHOICE_IN_NATIVE_QUIZ + INCORRECT_CHOICE,
        _(
            "Incorrect answer to multiple choice quiz with choices in native"
            " language"
        ),
    )
    SPELL_QUIZ_CORRECT = QuestionType.SPELL_QUIZ + CORRECT_CHOICE, _(
        "Correct answer to spelling quiz"
    )
    SPELL_QUIZ_INCORRECT = QuestionType.SPELL_QUIZ + INCORRECT_CHOICE, _(
        "Incorrect answer to spelling quiz"
    )
    SELECTION_FAMILIAR = QuestionType.FAMILIAR_SELECTION + CORRECT_CHOICE, _(
        "Word selected as familiar"
    )
    SELECTION_UNFAMILIAR = (
        QuestionType.FAMILIAR_SELECTION + INCORRECT_CHOICE,
        _("Word selected as unfamiliar"),
    )
    SELECTION_KNOWN = QuestionType.KNOWN_SELECTION + CORRECT_CHOICE, _(
        "Word selected as known"
    )
    SELECTION_UNKNOWN = QuestionType.KNOWN_SELECTION + INCORRECT_CHOICE, _(
        "Word selected as unknown"
    )


class SelectionType:
    NOT_MARKED = 1
    UNKNOWN = 2


class Languages(models.TextChoices):
    KYRGYZ = "KY", _("KYRGYZ")
    ENGLISH = "EN", _("ENGLISH")
    RUSSIAN = "RU", _("RUSSIAN")
