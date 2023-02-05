from django.test import TestCase

from rest_framework.test import APITestCase

from dance.const import Languages
from dance.models import Word
from dance.utils.csv_to_words_converter import save_words_to_db
from dance.vocabularies.vocabularies import TEST_VOCAB


class CSVtoWordsConverterTest(TestCase):
    def test_converter_no_translations(self):
        lines = TEST_VOCAB.splitlines()
        save_words_to_db(lines)
        self.assertEqual(
            Word.objects.all().count(),
            len(lines) - 1,
            "Wrong number of words created.",
        )

    def test_converter_with_translations(self):
        lines = TEST_VOCAB.splitlines()
        save_words_to_db(
            lines,
            translations_included=True,
            primary_language=Languages.ENGLISH,
        )
        english_words_count_in_db = (
            Word.objects.all().filter(language=Languages.ENGLISH).count()
        )
        english_words_count_in_vocab = TEST_VOCAB.count("EN")
        self.assertEqual(
            english_words_count_in_db,
            english_words_count_in_vocab,
            (
                "Numbers of english words in db and imported vocabulary do"
                " not match."
            ),
        )

        english_words_count_in_db = (
            Word.objects.all().filter(language=Languages.RUSSIAN).count()
        )
        english_words_count_in_vocab = TEST_VOCAB.count("RU")
        self.assertEqual(
            english_words_count_in_db,
            english_words_count_in_vocab,
            (
                "Numbers of russian words in db and imported vocabulary do"
                " not match."
            ),
        )

        for word in list(Word.objects.all()):
            # print(
            #     f"--------WORD: {word} TRANSLATION:"
            #     f" {word.translations.all()} -----------"
            # )
            self.assertGreater(
                word.translations.count(),
                0,
                "Not all words have translations after import.",
            )
