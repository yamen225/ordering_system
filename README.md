# ordering_system
A multi currency small ordering system.

Django based web application allows Admins to create products with price and currency, and normal users to buy them with
their own currencies.

Currency values are being updated on daily basis.

# Authentication
Using token authentication system, after logging in / registration will receive a token to ensure identity.
check swagger for user apis 

# Links
Docs are available on /api/docs/
swagger available on /api/swagger or /api/redoc

# Installation
Clone repo using: ```git clone https://github.com/yamen225/ordering_system.git``` <br>
on your terminal run: ```cd ordering_system``` <br>
create a python virtual env: ```python3.5 -m venv </path/to/your/venv>``` <br>
update pip by running: ```pip install --upgrade pip``` <br>
install requirements by running: ```pip install -r requirements.txt``` <br>
migrate db: ```python manage.py migrate``` <br>
create super user: ```python manage.py createsuperuser``` <br>
run dev server: ```python manage.py runserver``` <br>
