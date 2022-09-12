import datetime

from pydantic import *

from app.schemas.base import JsonSchema


class RegisterRequestSchema(JsonSchema):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class LoginRequestSchema(JsonSchema):
    email: EmailStr
    password: str


class AccessTokenResponseSchema(JsonSchema):
    access_token: str


class AuthDetailResponseSchema(AccessTokenResponseSchema):
    refresh_token: str
