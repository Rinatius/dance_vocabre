from .wordselector import select_words, select_translation, translate_words
from ..const import AnswerSheetType, SelectionType
from ..models import Word


def generate_questions(
    answersheet_type, learner, test_language, native_language, amount=10
):
    if answersheet_type == AnswerSheetType.QUIZ:
        words = select_words(
            learner, amount, test_language, SelectionType.UNKNOWN
        )
        questions, uischema, answers = generate_quiz(words, native_language)
    else:
        words = select_words(learner, amount, test_language)
        questions, uischema, answers = generate_selection_list(
            words, native_language
        )
    return questions, uischema, answers


# def generate_quiz(words, native_language):
#     questions = {"properties": {}}
#     answers = {}
#     uischema = {"ui:order": []}
#     for word in words:
#         translation = list(
#             select_translation(word, native_language).values_list(
#                 "word", flat=True
#             )
#         )
#         questions["properties"][word.word] = {
#             "type": "string",
#             "title": ", ".join(translation),
#         }
#         answers[word.word] = word.word
#         uischema["ui:order"].append(word.word)
#
#     return questions, uischema, answers


def make_spell_question(word, translation):
    question = {
        "type": "string",
        "title": ", ".join(translation),
    }
    answer = word
    return question, answer


def generate_quiz(words, native_language):
    questions = {"properties": {}}
    answers = {}
    uischema = {"ui:order": []}
    word_translations = translate_words(words, native_language)
    for word in word_translations:
        key = word["word"]
        questions["properties"][key], answers[key] = make_spell_question(
            word["word"], word["translations"]
        )
        uischema["ui:order"].append(key)

    return questions, uischema, answers


# def generate_options(word, words, translation, options_number, native_choices):
#     correct_answer = ", ".join(translation) if native_choices else word.word
#     options = [correct_answer]
#     return options, correct_answer


# def generate_multiple_choice_quiz(
#     words, native_language, native_choices=True, options_number=4
# ):
#     questions = {"properties": {}}
#     answers = {}
#     uischema = {"ui:order": []}
#     word_translations = {}
#
#
#
#     for word in words:
#         translation = list(
#             select_translation(word, native_language).values_list(
#                 "word", flat=True
#             )
#         )
#         word_translations[word]
#         question = word.word if native_choices else ", ".join(translation)
#         options, correct_answer = generate_options(
#             word,
#             words,
#             translation,
#             options_number,
#             native_choices=native_choices,
#         )
#         questions["properties"][word.word] = {
#             "type": "string",
#             "title": question,
#             "enum": options,
#         }
#         answers[word.word] = correct_answer
#         uischema["ui:order"].append(word.word)
#
#     return questions, uischema, answers


def generate_selection_list(words, native_language):
    questions = {"properties": {}}
    answers = {}
    uischema = {"ui:order": []}
    for word in words:
        questions["properties"][word.word] = {
            "type": "boolean",
            "title": word.word,
        }
        answers[word.word] = True
        uischema["ui:order"].append(word.word)

    return questions, uischema, answers
