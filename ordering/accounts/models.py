from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    currency = models.ForeignKey(
        'currencies.Currency', on_delete=models.CASCADE, related_name='users',
        help_text='currency of the user', null=True)
