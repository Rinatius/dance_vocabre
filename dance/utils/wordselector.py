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
            enocounters__in=learner_encounters.filter(
                encounter_type=EncounterType.SELECTION_UNKNOWN
            )
        ).exclude(
            enocounters__in=learner_encounters.filter(
                encounter_type=EncounterType.SELECTION_KNOWN
            )
        )
    elif selection_type == SelectionType.UNKNOWN:
        selected_words = selected_words.filter(
            enocounters__encounter_type=EncounterType.SELECTION_UNKNOWN
        )
    return selected_words.order_by("order")[:amount]
