import random

from .wordselector import translate_words
from ..const import QuestionType


def make_questions(words, answersheet_type, native_language):
    questions = {"properties": {}}
    answers = {}
    uischema = {"ui:order": []}

    # words = select_words_for_answersheet(words_pool, learner, answersheet_type)
    word_translations = translate_words(words, native_language)

    for word in word_translations:
        key = word["word"]
        questions["type"] = "object"
        questions["properties"][key], answers[key] = make_question(
            answersheet_type,
            word["word"],
            word["translations"],
            word_translations,
        )
        uischema["ui:order"].append(key)

    return questions, uischema, answers


def make_question(question_type, word, translation, all_word_translations):
    if question_type == QuestionType.SPELL_QUIZ:
        return make_spell_question(word, translation)
    elif question_type == QuestionType.MULTI_CHOICE_QUIZ:
        return make_multichoice_question(word, all_word_translations, 4, False)
    elif question_type == QuestionType.MULTI_CHOICE_IN_NATIVE_QUIZ:
        return make_multichoice_question(word, all_word_translations, 4, True)
    return make_selection_question(word, translation)


def make_spell_question(word, translation):
    question = {
        "type": "string",
        "title": ", ".join(translation),
    }
    answer = word
    return question, answer


def make_selection_question(word, translation):
    question = {
        "type": "boolean",
        "title": word,
    }
    answer = True
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
