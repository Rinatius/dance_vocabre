from django.contrib.auth.models import AbstractUser

from ..models.base import BaseDatesModel


class User(AbstractUser, BaseDatesModel):
    def __str__(self):
        return self.email
