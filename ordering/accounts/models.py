from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    # currency = models.ForeignKey(
    #     'currency.Currency', on_delete=models.CASCADE, related_name='products',
    #     help_text='currency of the product')
    # add additional fields in here
