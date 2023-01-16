from django.db import models


class ConText(models.Model):
    text = models.TextField(
            help_text="Text for the context"
            )

