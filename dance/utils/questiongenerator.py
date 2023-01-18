import json

from .wordselector import select_words


def generate_questions(questions_type, learner, amount):
    if questions_type == "qz":
        words = select_words(learner, amount)
        questions, uischema, answers = generate_quiz(words)
    else:
        words = select_words(learner, amount)
        questions, uischema, answers = generate_selection_list(words)
    return questions, uischema, answers


def generate_quiz(words):
    return "", "", ""


def generate_selection_list(words):
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
