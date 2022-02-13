# currencio
A Django sample project that exposes an API to convert currencies between EGP, EUR and USD

## To bootstrap project:
Run `docker-compose build && docker-compose up`

## To use the project:
1. Authenticate at `/api-token-auth/` with a POST request with payload:
```json
{
    "username": "api_user",
    "password": "api_user_password"
}
```
Then use the token as an Authorization header to the following request with prefix "Token"


2. To convert currencies at `/api/convert/`
with a `POST` request with payload as follows:
```json
{
    "from_currency": "EGP",
    "to_currency": "EUR",
    "amount": 10
}
```
