from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from dance.const import (
    Languages,
    QuestionType,
    EncounterType,
    INCORRECT_CHOICE,
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

    def create_answersheet(self, question_type):
        data = {
            "type": question_type,
            "learner": self.learner.pk,
            "test_language": Languages.ENGLISH,
            "native_language": Languages.RUSSIAN,
            "regenerate_stack": False,
            "stack_size": 10,
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
