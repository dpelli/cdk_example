# Standard Library Imports
from typing import List, Optional

# Third-Party Imports
from pydantic import BaseModel


class Subscription(BaseModel):
    plan: str
    status: str
    payment_method: str
    term: str


class CreditCard(BaseModel):
    cc_number: str


class Coordinates(BaseModel):
    lat: str
    lng: str


class Address(BaseModel):
    city: str
    street_name: str
    street_address: str
    zip_code: str
    state: str
    country: str


class Employment(BaseModel):
    title: str
    key_skill: str


class User(BaseModel):
    id: int
    uid: str
    password: str
    first_name: str
    last_name: str
    username: str
    email: str
    avatar: str
    gender: str
    phone_number: str
    social_insurance_number: str
    date_of_birth: str
    # employment: Employment
    # address: Address
    # credit_card: CreditCard
    # subscription: Subscription
