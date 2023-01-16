import json

from .wordselector import select_words


def generate_questions(questions_type, learner, amount):
    words = select_words(learner, questions_type, amount)
    if questions_type == "qz":
        questions, uischema, answers = generate_quiz(words)
    else:
        questions, uischema, answers = generate_selection_list(words)
    return questions, uischema, answers


def generate_quiz(words):
    return "", "", ""


def generate_selection_list(words):
    questions = {"properties": {}}
    answers = {}
    uischema = {"ui:order": []}
    for word in words:
        questions["properties"][word] = {"type": "boolean", "title": word.word}
        answers[word] = True
        uischema["ui:order"].append(word)

    return json.dumps(questions), json.dumps(uischema), json.dumps(answers)
