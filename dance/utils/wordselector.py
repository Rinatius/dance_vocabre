from ..models import Encounter
from ..models import Word
from ..const import SelectionType, EncounterType
from ..default_settings import WORD_KNOWN_ENCOUNTERS


def select_words(
    learner,
    amount,
    language=None,
    selection_type=SelectionType.NOT_MARKED,
    collection=None,
):
    selected_words = (
        collection.words.all()
        if collection is not None
        else Word.objects.all()
    )
    if language:
        selected_words = selected_words.filter(language=language)
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
        word_known_encounter_types = [EncounterType.SELECTION_KNOWN]
        word_known_encounter_types.extend(WORD_KNOWN_ENCOUNTERS)
        selected_words = selected_words.filter(
            encounters__in=learner_encounters.filter(
                encounter_type=EncounterType.SELECTION_UNKNOWN
            )
        ).exclude(
            encounters__in=learner_encounters.filter(
                encounter_type__in=word_known_encounter_types
            )
        )

    return selected_words.order_by("order")[:amount]


# def select_words(
#     learner, language, selection_type=SelectionType.NOT_MARKED, amount=10
# ):
#     selected_words = Word.objects.all().filter(language=language)
#     learner_encounters = Encounter.objects.all().filter(learner=learner)
#     if selection_type == SelectionType.NOT_MARKED:
#         selected_words = exclude_words_by_encounter_types(
#             selected_words,
#             learner_encounters,
#             [EncounterType.SELECTION_UNKNOWN, EncounterType.SELECTION_KNOWN],
#         )
#     if selection_type == SelectionType.UNKNOWN:
#         selected_words = include_words_by_encounter_types(
#             selected_words,
#             learner_encounters,
#             [EncounterType.SELECTION_UNKNOWN],
#         )
#         selected_words
#     return selected_words.order_by("order")[:amount]
#
#
# def include_words_by_encounter_types(words, encounters, encounter_types):
#     words_queryset = words
#     for encounter_type in encounter_types:
#         words_queryset = words_queryset.filter(
#             encounters__in=encounters.filter(encounter_type=encounter_type)
#         )
#     return words_queryset
#
#
# def exclude_words_by_encounter_types(words, encounters, encounter_types):
#     words_queryset = words
#     for encounter_type in encounter_types:
#         words_queryset = words_queryset.exclude(
#             encounters__in=encounters.filter(encounter_type=encounter_type)
#         )
#     return words_queryset


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


def select_new_stack(learner, language, collection):

    return None
