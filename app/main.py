import os
import time
import uuid
from typing import Dict

import requests
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from requests_oauthlib import OAuth1
from .auth import create_access_token, get_current_user

app = FastAPI()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
PESAPAL_IFRAME_URL = "https://cybqa.pesapal.com/pesapalv3"


class User(BaseModel):
  username: str
  password: str

class CustomerData(BaseModel):
  amount: int
  description: str
  email: str
  phone_number: str
  currency: str


@app.get("/")
def read_homepage():
  return {"message": "Welcome to the Pesapal Iframe Generator"}


@app.get("/healthz")
def health_check():
  return {"status": "healthy"}


@app.post("/login")
def login(form_data: User):
  if form_data.username == "admin" and form_data.password == "password":
    return {"access_token": create_access_token(data={"sub": form_data.username}), "token_type": "bearer"}
  else:
    raise HTTPException(status_code=400, detail="Invalid credentials")


def generate_iframe_url(transaction_details: Dict):
    """
    Generates the Pesapal iframe URL for the payment interface.

    Args:
        transaction_details (Dict): A dictionary containing transaction details.

    Returns:
        str: The iframe URL.

    Raises:
        HTTPException: If there is an error generating the iframe URL.
    """

    oauth_nonce = str(uuid.uuid4())
    oauth_timestamp = int(time.time())

    oauth = OAuth1(
        client_key=CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        signature_type="query",
        nonce=oauth_nonce,
        timestamp=str(oauth_timestamp)
    )

    try:
        response = requests.post(PESAPAL_IFRAME_URL, auth=oauth, data=transaction_details)
        response.raise_for_status()

        iframe_url = response.url
        return iframe_url

    except requests.exceptions.RequestException as e:
        print(f"Error generating iframe URL: {e}")
        return None


@app.post("/get-pesapal-iframe")
def get_pesapal_iframe(
    customer_data: CustomerData,
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint to generate a Pesapal iframe URL based on customer data.

    Args:
        customer_data (CustomerData): Data from the customer.
        current_user (User): The currently authenticated user.

    Returns:
        Dict: A dictionary with the iframe URL and a success message.
    """
    transaction_details = {
        "Type": "MERCHANT",
        "Reference": "123456789",
        "CallbackUrl": "https://yourwebsite.com/callback",
        "Amount": customer_data.amount,
        "Description": customer_data.description,
        "Email": customer_data.email,
        "PhoneNumber": customer_data.phone_number
    }

    iframe_url = generate_iframe_url(transaction_details)
    return {"message": "Pesapal iframe URL generated successfully", "iframe_url": iframe_url}


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
