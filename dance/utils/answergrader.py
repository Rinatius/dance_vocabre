from ..const import (
    QuestionType,
    EncounterType,
    CORRECT_CHOICE,
    INCORRECT_CHOICE,
)
from ..models import Word, Encounter


def grade(questions, correct_answers, given_answers):
    return 100


def normalize(answer):
    return answer


def generate_encounter(learner, word_key, correct, question_type):
    word = Word.objects.get(word=word_key)
    # TODO: Possibly remove this request by using word id for optimization.

    encounter_type = (
        question_type + CORRECT_CHOICE if correct else INCORRECT_CHOICE
    )
    return Encounter(word=word, learner=learner, encounter_type=encounter_type)


def generate_encounter_and_score(
    answersheet, correct_answer_key, learner_answer
):
    encounters = []
    correct = False
    answer = answersheet.correct_answers[correct_answer_key]
    if normalize(answer) == normalize(learner_answer):
        correct = True
    if answersheet.type == QuestionType.KNOWN_SELECTION:
        encounters.append(
            generate_encounter(
                answersheet.learner,
                correct_answer_key,
                correct,
                answersheet.type,
            )
        )
    return encounters, 1 if correct else 0


def generate_encounters_and_score(answersheet, learner_answers):
    score = 0
    encounters = []
    for answer in answersheet.correct_answers:
        if answer in learner_answers:
            encounter, point = generate_encounter_and_score(
                answersheet, answer, learner_answers[answer]
            )
            score += point
            encounters.extend(encounter)
    return encounters, round(score / len(answersheet.correct_answers) * 100)
