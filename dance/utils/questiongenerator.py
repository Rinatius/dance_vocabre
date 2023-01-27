import random

from .wordselector import select_words, select_translation, translate_words
from ..const import AnswerSheetType, SelectionType


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


def make_spell_question(word, translation):
    question = {
        "type": "string",
        "title": ", ".join(translation),
    }
    answer = word
    return question, answer


def make_multichoice_question(
    word, word_translations, options_number=4, options_in_native=True
):
    correct_answer = ""
    title = ""
    options = []
    for word_translation in word_translations:
        option = (
            ", ".join(word_translation["translations"])
            if options_in_native
            else word_translation["word"]
        )
        if word_translation["word"] == word:
            correct_answer = option
            title = (
                word_translation["word"]
                if options_in_native
                else ", ".join(word_translation["translations"])
            )
        else:
            options.append(option)

    options = random.sample(
        options,
        options_number - 1 if options_number < len(options) else len(options),
    )
    options.append(correct_answer)
    options = random.sample(options, len(options))
    question = {
        "type": "string",
        "title": title,
        "enum": options,
    }
    answer = correct_answer
    return question, answer


def generate_quiz(words, native_language):
    questions = {"properties": {}}
    answers = {}
    uischema = {"ui:order": []}
    word_translations = translate_words(words, native_language)
    for word in word_translations:
        key = word["word"]
        # questions["properties"][key], answers[key] = make_spell_question(
        #     word["word"], word["translations"]
        # )
        questions["properties"][key], answers[key] = make_multichoice_question(
            word["word"], word_translations
        )
        uischema["ui:order"].append(key)

    return questions, uischema, answers


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
