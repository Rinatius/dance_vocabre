from ..models import Encounter
from ..models import Word
from ..const import SelectionType, EncounterType


def select_words(
    learner, amount, language, selection_type=SelectionType.NOT_MARKED
):
    selected_words = Word.objects.all().filter(language=language)
    learner_encounters = Encounter.objects.all().filter(learner=learner)
    if selection_type == SelectionType.NOT_MARKED:
        selected_words = selected_words.exclude(
            encounters__in=learner_encounters.filter(
                encounter_type=EncounterType.SELECTION_UNKNOWN
            )
        ).exclude(
            encounters__in=learner_encounters.filter(
                encounter_type=EncounterType.SELECTION_KNOWN
            )
        )
    elif selection_type == SelectionType.UNKNOWN:
        selected_words = selected_words.filter(
            encounters__in=learner_encounters.filter(
                encounter_type=EncounterType.SELECTION_UNKNOWN
            )
        )
    return selected_words.order_by("order")[:amount]


def select_translations(words, language):
    translations = (
        Word.objects.all()
        .filter(language=language)
        .filter(translations__in=words)
    )
    return translations


def select_translation(word, language):
    translations = (
        Word.objects.all().filter(language=language).filter(translations=word)
    )
    return translations


def translate_words(words, language):
    return [
        {
            "word": word.word,
            "translations": list(
                word.translations.all()
                .filter(language=language)
                .values_list("word", flat=True)
            ),
        }
        for word in words
    ]
