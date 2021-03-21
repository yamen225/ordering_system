import requests
from django.conf import settings
from .models import Currency


def update_currencies():
    response = requests.get(f'http://data.fixer.io/api/latest?access_key={settings.FIXER_KEY}')
    try:
        for key, val in response.json()['rates']:
            Currency.objects.update_or_create(code=key, value=val)
    except Exception as e:
        print(e.__str__())
    return True
