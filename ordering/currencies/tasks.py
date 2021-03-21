import requests
from .models import Currency


def update_currencies():
    response = requests.get('http://data.fixer.io/api/latest?access_key=76a7def5eac09cedec5ad8d5052aa608')
    try:
        for key, val in response.json()['rates']:
            Currency.objects.update_or_create(code=key, value=val)
    except Exception as e:
        print(e.__str__())
    return True
