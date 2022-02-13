# currencio
A Django sample project that exposes an API to convert currencies between EGP, EUR and USD

## To bootstrap project:
### Using Docker:
Run `docker-compose build && docker-compose up`

### Using venv:
1. Create a virtual python environment using you preferred module and activate it
2. Run `pip install -r requirements.txt`

### Following either of the above;
1. Run `python manage.py migrate`
2. Run `python manage.py createsuperuser` and follow the interactive prompts to create a superuser
3. Run `python manage.py runserver` to start the server

Then you can either login into admin and create a new user to test the API with, or user the superuser you just created.

## To run tests:
### Using Docker Compose:
Run `docker-compose run --rm web ./manage.py test`

### In a venv:
Run `python manage.py test`

## To use the project:
1. Authenticate at `/api/api-token-auth/` with a POST request with payload:
```json
{
    "username": "api_user",
    "password": "api_user_password"
}
```
Then use the token as an Authorization header to the following request with prefix "Token"

An example token authorization header would be `Authorization: Token 2b882f2a79f4bdade349b0dfeeff19bee4834a29` 


2. To convert currencies at `/api/convert/`
with a `POST` request.

### Example Request:
```json
{
    "from_currency": "EGP",
    "to_currency": "EUR",
    "amount": 10
}
```

### Example response to above request:
```json
{
    "from_currency": "EGP",
    "to_currency": "EUR",
    "original_amount": 10.0,
    "converted_amount": 0.5607848116144366
}
```
