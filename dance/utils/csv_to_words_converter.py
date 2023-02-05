import csv

from dance.const import Languages
from dance.models import Word


class InvalidVocabularyFormatException(Exception):
    pass


# TODO Add more exceptions to ensure integrity of vocabulary
def save_words_to_db(
    vocab_string,
    skip_first_line=True,
    translations_included=False,
    primary_language=Languages.ENGLISH,
):
    vocab_list = list(csv.reader(vocab_string))
    if skip_first_line:
        vocab_list.pop(0)

    for word in vocab_list:
        new_word, created = Word.objects.get_or_create(
            defaults={"order": word[2]}, word=word[0], language=word[1]
        )
        if translations_included:
            if new_word.language == primary_language:
                word_to_translate = new_word
            try:
                if word_to_translate != new_word:
                    word_to_translate.translations.add(new_word)
            except NameError:
                raise InvalidVocabularyFormatException(
                    "Vocabulary does not start with word in primary language"
                    " when translations included is set to True."
                )
