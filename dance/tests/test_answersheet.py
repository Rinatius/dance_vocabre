from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from dance.const import Languages, QuestionType
from dance.models import Learner, System, AnswerSheet
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

    def test_creation(self):
        for question_type in QuestionType.choices:
            response = self.create_answersheet(question_type[0])
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
                AnswerSheet.objects.count(),
                1,
                (
                    f"{AnswerSheet.objects.count()} answersheets created"
                    " instead of 1 for {question_type[1]} question type."
                ),
            )
