from ..models import Encounter
from ..models import Word
from ..const import SelectionType, EncounterType


def select_words(learner, amount, selection_type=SelectionType.NOT_MARKED):
    selected_words = Word.objects.all()
    learner_encounters = Encounter.objects.all().filter(learner=learner)
    if selection_type == SelectionType.NOT_MARKED:
        selected_words = (
            selected_words.exclude(
                enocounters__in=learner_encounters.filter(
                    encounter_type=EncounterType.SELECTION_UNKNOWN
                )
            )
            .exclude(
                enocounters__in=learner_encounters.filter(
                    encounter_type=EncounterType.SELECTION_KNOWN
                )
            )
            .order_by("order")
        )[:amount]
    return selected_words
