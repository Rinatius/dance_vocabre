import csv

from dance.const import Languages
from dance.models import Word


def convert(
    vocab_string,
    skip_first_line=True,
    translations_included=False,
    primary_language=Languages.ENGLISH,
):
    vocab_list = list(csv.reader(vocab_string))
    if skip_first_line:
        poped = vocab_list.pop(0)
        print(poped)

    print(vocab_list[0])

    for word in vocab_list:
        new_word, created = Word.objects.get_or_create(
            defaults={"order": word[2]}, word=word[0], language=word[1]
        )
        if translations_included:
            word_to_translate = None
            if new_word.language == primary_language:
                word_to_translate = new_word
            elif word_to_translate is not None:
                word_to_translate.translations.add(new_word)
