from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from dance.const import (
    Languages,
    QuestionType,
    EncounterType,
    INCORRECT_CHOICE,
    CORRECT_CHOICE,
)
from dance.models import Learner, System, AnswerSheet, Encounter, Word
from dance.utils.csv_to_words_converter import save_words_to_db
from dance.vocabularies.vocabularies import TEST_VOCAB


class AnswerSheetTest(APITestCase):
    def setUp(self) -> None:
        lines = TEST_VOCAB.splitlines()
        save_words_to_db(
            lines,
            translations_included=True,
            primary_language=Languages.ENGLISH,
        )
        self.system = System.objects.create()
        self.learner = Learner.objects.create(
            external_id=1, system=self.system
        )
        self.client = APIClient()

    def create_answersheet(
        self, question_type, stack_size=10, regenerate_stack=False
    ):
        data = {
            "type": question_type,
            "learner": self.learner.pk,
            "test_language": Languages.ENGLISH,
            "native_language": Languages.RUSSIAN,
            "regenerate_stack": regenerate_stack,
            "stack_size": stack_size,
        }
        return self.client.post(reverse("answersheet-list"), data=data)

    def compare_content(self, content, response):
        saved_answersheet = AnswerSheet.objects.get(pk=response.data["id"])

        reference_questions = content["questions"]["properties"]
        response_questions = response.data["questions"]["properties"]
        saved_questions = saved_answersheet.questions["properties"]

        self.assertEqual(
            reference_questions,
            response_questions,
            (
                "Generated questions in response do not match reference ones. "
                f"Questions in response: {response_questions}\n"
                f"Reference questions: {reference_questions}"
            ),
        )

        self.assertEqual(
            reference_questions,
            saved_questions,
            (
                "Generated questions saved in db do not match reference ones. "
                f"Questions saved in db: {saved_questions}\n"
                f"Reference questions: {reference_questions}"
            ),
        )

        reference_uischema = content["uischema"]
        response_uischema = response.data["uischema"]
        saved_uischema = saved_answersheet.uischema

        self.assertEqual(
            reference_uischema,
            response_uischema,
            (
                "Generated uischema in response do not match reference one. "
                f"Uischema in response: {response_uischema}\n"
                f"Reference uischema: {reference_uischema}"
            ),
        )

        self.assertEqual(
            reference_questions,
            saved_questions,
            (
                "Generated uischema saved in db do not match reference one."
                f"Uischema saved in db: {saved_uischema}\n"
                f"Reference uischema: {reference_uischema}"
            ),
        )

        reference_correct_answers = content["correct_answers"]
        saved_correct_answers = saved_answersheet.correct_answers

        self.assertEqual(
            reference_correct_answers,
            saved_correct_answers,
            (
                "Generated correct answers saved in db do not match reference"
                " ones.\nCorrect answers in db:"
                f" {response_uischema}\nReference correct"
                f" answers:{reference_uischema}"
            ),
        )

    def check_contents_no_encounters(self, response):
        content = {
            "questions": {"properties": {}},
            "uischema": {"ui:order": []},
            "correct_answers": {},
        }

        self.compare_content(content, response)

    def check_content(self, question_type, content):
        response = self.create_answersheet(question_type)

        self.check_contents_no_encounters(response)

        for word in content["uischema"]["ui:order"]:
            Encounter(
                learner=self.learner,
                encounter_type=EncounterType.SELECTION_UNKNOWN,
                word=Word.objects.get(word=word),
            ).save()
        response = self.create_answersheet(question_type)
        self.compare_content(content, response)

    def test_creation(self):
        for i, question_type in enumerate(QuestionType.choices):
            response = self.create_answersheet(question_type[0])
            sheets_count = AnswerSheet.objects.filter(
                type=question_type[0]
            ).count()
            sheets_total_count = AnswerSheet.objects.count()
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                (
                    f"Wrong response code, for {question_type[1]} question"
                    f" type, expected: {status.HTTP_201_CREATED}, received:"
                    f" {response.status_code} "
                ),
            )

            self.assertEqual(
                sheets_count,
                1,
                (
                    f"{sheets_count} answersheets created instead of 1 for"
                    f" {question_type[1]} question type."
                ),
            )

            self.assertEqual(
                sheets_total_count,
                i + 1,
                (
                    f"{sheets_total_count} answersheets created instead of"
                    f" {i+1} for {question_type[1]} question type."
                ),
            )

    def test_contents_selection_known(self):
        response = self.create_answersheet(QuestionType.KNOWN_SELECTION)

        content = {
            "questions": {
                "properties": {
                    "go": {"type": "boolean", "title": "go"},
                    "car": {"type": "boolean", "title": "car"},
                    "sun": {"type": "boolean", "title": "sun"},
                    "rain": {"type": "boolean", "title": "rain"},
                    "road": {"type": "boolean", "title": "road"},
                    "snow": {"type": "boolean", "title": "snow"},
                    "wind": {"type": "boolean", "title": "wind"},
                    "house": {"type": "boolean", "title": "house"},
                    "human": {"type": "boolean", "title": "human"},
                    "people": {"type": "boolean", "title": "people"},
                }
            },
            "uischema": {
                "ui:order": [
                    "car",
                    "house",
                    "go",
                    "people",
                    "human",
                    "rain",
                    "road",
                    "sun",
                    "snow",
                    "wind",
                ]
            },
            "correct_answers": {
                "go": True,
                "car": True,
                "sun": True,
                "rain": True,
                "road": True,
                "snow": True,
                "wind": True,
                "house": True,
                "human": True,
                "people": True,
            },
        }

        self.compare_content(content, response)

    def test_content_selection_familiar(self):
        content = {
            "questions": {
                "properties": {
                    "go": {"type": "boolean", "title": "go"},
                    "car": {"type": "boolean", "title": "car"},
                    "sun": {"type": "boolean", "title": "sun"},
                    "rain": {"type": "boolean", "title": "rain"},
                    "road": {"type": "boolean", "title": "road"},
                    "snow": {"type": "boolean", "title": "snow"},
                    "wind": {"type": "boolean", "title": "wind"},
                    "house": {"type": "boolean", "title": "house"},
                    "human": {"type": "boolean", "title": "human"},
                    "people": {"type": "boolean", "title": "people"},
                }
            },
            "uischema": {
                "ui:order": [
                    "car",
                    "house",
                    "go",
                    "people",
                    "human",
                    "rain",
                    "road",
                    "sun",
                    "snow",
                    "wind",
                ]
            },
            "correct_answers": {
                "go": True,
                "car": True,
                "sun": True,
                "rain": True,
                "road": True,
                "snow": True,
                "wind": True,
                "house": True,
                "human": True,
                "people": True,
            },
        }

        self.check_content(QuestionType.FAMILIAR_SELECTION, content)

    def test_content_spelling(self):
        content = {
            "questions": {
                "properties": {
                    "car": {"type": "string", "title": "машина, автомобиль"},
                    "house": {"type": "string", "title": "дом"},
                    "go": {"type": "string", "title": "идти, ехать"},
                    "people": {"type": "string", "title": "люди, народ"},
                    "human": {"type": "string", "title": "человек"},
                    "rain": {"type": "string", "title": "дождь"},
                    "road": {"type": "string", "title": "дорога"},
                    "sun": {"type": "string", "title": "солнце"},
                    "snow": {"type": "string", "title": "снег"},
                    "wind": {"type": "string", "title": "ветер"},
                }
            },
            "correct_answers": {
                "go": "go",
                "car": "car",
                "sun": "sun",
                "rain": "rain",
                "road": "road",
                "snow": "snow",
                "wind": "wind",
                "house": "house",
                "human": "human",
                "people": "people",
            },
            "uischema": {
                "ui:order": [
                    "car",
                    "house",
                    "go",
                    "people",
                    "human",
                    "rain",
                    "road",
                    "sun",
                    "snow",
                    "wind",
                ]
            },
        }

        self.check_content(QuestionType.SPELL_QUIZ, content)

    def check_encounters_number(
        self, word_key, question_type, correct_count=1, incorrect_count=1
    ):
        encounter_correct_count = Encounter.objects.filter(
            word__word=word_key,
            encounter_type=(question_type + CORRECT_CHOICE),
        ).count()
        encounter_incorrect_count = Encounter.objects.filter(
            word__word=word_key,
            encounter_type=(question_type + INCORRECT_CHOICE),
        ).count()

        self.assertEqual(
            encounter_correct_count,
            correct_count,
            (
                "Incorrect number of encounters for correct answer to"
                f" {QuestionType} type question created."
            ),
        )
        self.assertEqual(
            encounter_incorrect_count,
            incorrect_count,
            (
                "Incorrect number of encounters for incorrect answer to"
                f" {question_type} type question created."
            ),
        )

    def check_answersheet_answering(
        self,
        answersheet_id,
        correct_answer_key="go",
        incorrect_answer_key="car",
        correct_answer=True,
        incorrect_answer=False,
    ):
        data = {"learner_answers": {}}
        data["learner_answers"][correct_answer_key] = correct_answer
        data["learner_answers"][incorrect_answer_key] = incorrect_answer
        answers_update_url = reverse(
            "answersheet-detail", kwargs={"pk": answersheet_id}
        )

        response = self.client.patch(answers_update_url, data, format="json")
        question_type = response.data["type"]

        self.check_encounters_number(
            question_type=question_type,
            word_key=correct_answer_key,
            correct_count=1,
            incorrect_count=0,
        )
        self.check_encounters_number(
            question_type=question_type,
            word_key=incorrect_answer_key,
            correct_count=0,
            incorrect_count=1,
        )

        self.assertEqual(
            response.data["score"],
            10,
            (
                f"Answersheet score calculated incorrectly for {question_type}"
                " type answersheet."
            ),
        )

    def mark_as(self, known=False, words_count=10):
        response = self.create_answersheet(
            QuestionType.KNOWN_SELECTION,
            stack_size=words_count,
            regenerate_stack=True,
        )
        answersheet_id = response.data["id"]
        answersheet = AnswerSheet.objects.get(pk=answersheet_id)
        answers = answersheet.correct_answers
        if not known:
            for word in answersheet.correct_answers:
                answers[word] = not answersheet.correct_answers[word]

        data = {"learner_answers": answers}
        answers_update_url = reverse(
            "answersheet-detail", kwargs={"pk": answersheet_id}
        )
        return self.client.patch(answers_update_url, data, format="json")

    def mark_as_unknown(self, words_count=10):
        return self.mark_as(known=False, words_count=words_count)

    def mark_as_known(self, words_count=10):
        return self.mark_as(known=True, words_count=words_count)

    def test_mark_as_unknown(self):
        response = self.mark_as_unknown(10)
        for word in response.data["uischema"]["ui:order"]:
            self.check_encounters_number(
                word_key=word,
                question_type=QuestionType.KNOWN_SELECTION,
                correct_count=0,
                incorrect_count=1,
            )
        self.assertEqual(response.data["score"], 0)

    def test_mark_as_known(self):
        response = self.mark_as_known(10)
        for word in response.data["uischema"]["ui:order"]:
            self.check_encounters_number(
                word_key=word,
                question_type=QuestionType.KNOWN_SELECTION,
                correct_count=1,
                incorrect_count=0,
            )
        self.assertEqual(response.data["score"], 100)

    def test_answersheet_answering(self):
        unknown_number = 10
        self.mark_as_unknown(unknown_number)
        question_types = [
            QuestionType.FAMILIAR_SELECTION,
            QuestionType.MULTI_CHOICE_QUIZ,
            QuestionType.MULTI_CHOICE_IN_NATIVE_QUIZ,
            QuestionType.SPELL_QUIZ,
        ]

        for question_type in question_types:
            response = self.create_answersheet(
                question_type, regenerate_stack=True
            )

            correct_answer_key = "go"
            incorrect_answer_key = "car"
            correct_answer = True
            incorrect_answer = False

            if (
                question_type == QuestionType.SPELL_QUIZ
                or question_type == QuestionType.MULTI_CHOICE_QUIZ
            ):
                correct_answer = "go"
                incorrect_answer = "carrrr"
            elif question_type == QuestionType.MULTI_CHOICE_IN_NATIVE_QUIZ:
                correct_answer = "идти, ехать"
                incorrect_answer = "мшина"

            self.check_answersheet_answering(
                response.data["id"],
                correct_answer_key,
                incorrect_answer_key,
                correct_answer,
                incorrect_answer,
            )
            answersheet_without_regenerate = self.create_answersheet(
                question_type, regenerate_stack=False
            )
            self.assertNotIn(
                correct_answer_key,
                answersheet_without_regenerate.data["uischema"]["ui:order"],
                (
                    "Question that was answered correctly is included into"
                    " answersheet without stack regeneration for"
                    f" {question_type} question type"
                ),
            )
            self.assertIn(
                incorrect_answer_key,
                answersheet_without_regenerate.data["uischema"]["ui:order"],
                (
                    "Question that was answered incorrectly is not included"
                    " into answersheet without stack regeneration for"
                    f" {question_type} question type"
                ),
            )
            answersheet_with_regenerate = self.create_answersheet(
                question_type, regenerate_stack=True
            )
            if question_type == QuestionType.SPELL_QUIZ:
                self.assertNotIn(
                    correct_answer_key,
                    answersheet_with_regenerate.data["uischema"]["ui:order"],
                    (
                        "Question that was answered correctly is included"
                        " into answersheet with stack regeneration for"
                        f" {question_type} question type"
                    ),
                )
            else:
                self.assertIn(
                    correct_answer_key,
                    answersheet_with_regenerate.data["uischema"]["ui:order"],
                    (
                        "Question that was answered correctly is NOT included"
                        " into answersheet with stack regeneration for"
                        f" {question_type} question type"
                    ),
                )
            self.assertIn(
                incorrect_answer_key,
                answersheet_with_regenerate.data["uischema"]["ui:order"],
                (
                    "Question that was answered incorrectly is not"
                    " included into answersheet with stack regeneration for"
                    f" {question_type} question type"
                ),
            )

        self.assertEqual(
            Encounter.objects.count(),
            len(QuestionType.choices) * 2
            + unknown_number
            - 2,  # One correct and one incorrect encounter for all
            # question types (this test will fail if new question type
            # is added but not tested) excluding Known Selection type plus
            # all incorrect known selection encounters that were created
            # previously
            "Incorrect number of encounters created.",
        )
