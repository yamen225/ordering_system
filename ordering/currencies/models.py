from django.db import models
from datetime import date


class Currency(models.Model):
    """Store the value of currencies compared to Euro"""

    code = models.CharField(unique=True, max_length=10, help_text="currency code")
    value = models.FloatField(default=1, help_text="current value compared to Eur")
    last_updated = models.DateField(auto_now=True, help_text="Store tha last time the value got updated.")

    @staticmethod
    def updating_latest_values(cls):
        """Update the currencies daily"""
        from .tasks import update_currencies
        today = date.today()
        if not cls.objects.first().last_update == today:
            update_currencies()
        return True
