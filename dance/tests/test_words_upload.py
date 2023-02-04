from rest_framework.test import APITestCase

from dance.models import Word
from dance.utils.csv_to_words_converter import convert
from dance.vocabularies.vocabularies import TEST_VOCAB


class CSVtoWordsConverterTest(APITestCase):
    def test_converter_no_translations(self):
        lines = TEST_VOCAB.splitlines()
        convert(lines)
        self.assertEqual(
            Word.objects.all().count(),
            len(lines) - 1,
            "Wrong number of words created.",
        )
