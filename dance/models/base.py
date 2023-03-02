from django.db import models


class BaseDatesModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Time of creation"
    )

    updated_at = models.DateTimeField(
        auto_now=True, help_text="Last update time"
    )

    class Meta:
        abstract = True
