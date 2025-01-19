# pesapal-iframe-generator
This service is a python FastApi service that accept product and customer details and returns an iframe url to complete payments.

The logic is built using [python fastapi framework](https://fastapi.tiangolo.com/)

This service assumes a theoritial microservice that accepts customer data for ecommerce product purchase like amount,currency, email, product description and does uses the pesapal iframe generation url to generate an iframe url. The request is authenticated using oauth with merchant consumer key and secret.

## Running the project

Create an isolated environment for our code

```sh
python3 -m venv .venv

```

Activate the virtual environment

```sh
source .venv/bin/activate

```

Install Dependencies
```sh
pip install -r requirements.txt

```

In the source directory, run the project using this command. Ensure to export the pesapal merchant consumer key and secret.

```sh
export CONSUMER_KEY="xxxxx"
export CONSUMER_SECRET="xxx"

uvicorn app.main:app --reload --port 8000
```

## Working with the api

There is a [VSCode rest client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) spec definition at the [root of the project](./client.http) that has instructions to work with the api.

The username `admin` and password `password` has been hardcoded to simplify the API working and keep the focus on generating jwt token and generating the iframe url.

To Authenticate with the api, use the `/login` endpoint

```sh
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
      "username": "admin",
      "password": "password"
  }'
```

You should get a json response like this

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTczNjYwNzIzMX0.6ZgNVtWd29r8Kbl-J3Ugp31D7YTvDGR7ipEYMWWQLlM",
  "token_type": "bearer"
}
```

To generate an iframe, use the generated `access_token` in the header like this

```sh
curl -X POST http://127.0.0.1:8000/get-pesapal-iframe \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTczNjYwNzIzMX0.6ZgNVtWd29r8Kbl-J3Ugp31D7YTvDGR7ipEYMWWQLlM" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
      "amount": "1900",
      "description": "Small piece of wood purchase.",
      "email": "hillary.korir@gmail.com",
      "phone_number": "254700000010",
      "currency": "KES"
  }'
```

The response is a json with the generated iframe url, like shown here

```json
{
  "message": "Pesapal iframe URL generated successfully",
  "iframe_url": "https://www.pesapal.com/API/PostPesapalDirectOrderV4?oauth_nonce=65d5d170-114c-4e78-80bc-ca6322a41d91&oauth_timestamp=1736603789&oauth_version=1.0&oauth_signature_method=HMAC-SHA1&oauth_consumer_key=PjYSPVrROoGzoUznGY1WIFZrZU57%2BF0P&oauth_signature=iAuWKS3e4Up7S60Z5w%2BTMLIjv9Y%3D"
}
```

## Docs

The open api spec for the api can be found in the docs endpoint - <http://127.0.0.1:8000/docs>
