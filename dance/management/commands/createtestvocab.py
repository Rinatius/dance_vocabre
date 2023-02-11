from django.core.management import BaseCommand, CommandError

from dance.const import Languages
from dance.utils.csv_to_words_converter import save_words_to_db
from dance.vocabularies.vocabularies import TEST_VOCAB


class Command(BaseCommand):
    help = "Creates words from test vocabulary"

    def handle(self, *args, **options):
        try:
            lines = TEST_VOCAB.splitlines()
            save_words_to_db(
                lines,
                translations_included=True,
                primary_language=Languages.ENGLISH,
            )
        # TODO Rewrite except
        except:
            raise CommandError("Vocab was not create")
        self.stdout.write(
            self.style.SUCCESS("Successfully created vocabulary")
        )
