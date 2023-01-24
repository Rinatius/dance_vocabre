from .wordselector import select_words
from ..const import AnswerSheetType, SelectionType
from ..models import Word


def generate_questions(
    answersheet_type, learner, amount, test_language, native_language
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


def generate_quiz(words, native_language):
    questions = {"properties": {}}
    answers = {}
    uischema = {"ui:order": []}
    translations = Word.objects.all().filter(native_language=native_language)
    translation_dicts = set(
        {"translations": translation.translations, "word": translation.word}
        for translation in translations
    )
    for word in words:
        translation = [
            translation_dict["word"]
            for translation_dict in translation_dicts
            if word.id in translation_dict["translations"]
        ]
        questions["properties"][word.word] = {
            "type": "string",
            "title": ", ".join(translation),
        }
        answers[word.word] = True
        uischema["ui:order"].append(word.word)

    return "", "", ""


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
