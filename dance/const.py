from enum import Enum
from django.db import models
from django.utils.translation import gettext_lazy as _


class AnswerSheetType(models.TextChoices):
    QUIZ = "QZ", _("Quiz")
    FAMILIAR_SELECTION = "FS", _("Familiar selection")
    KNOWN_SELECTION = "KS", _("Known selection")


class EncounterType(models.TextChoices):
    PURE_CONTEXT = "PC", _("Pure context")
    QUIZ_CONTEXT = "QC", _("Quiz context")
    QUIZ_TARGET = "QT", _("Quiz target")
    QUIZ_OPTIONS = "QO", _("Quiz options")
    QUIZ_INCORRECT = "QI", _("Quiz incorrect answer")
    SELECTION_KNOWN = "SK", _("Selection known")
    SELECTION_UNKNOWN = "SU", _("Selection unknown")


class SelectionType(Enum):
    NOT_MARKED = 1
    UNKNOWN = 2


class Languages(models.TextChoices):
    KYRGYZ = "KY", _("KYRGYZ")
    ENGLISH = "EN", _("ENGLISH")
    RUSSIAN = "RU", _("RUSSIAN")
