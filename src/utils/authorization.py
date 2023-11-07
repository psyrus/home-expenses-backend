from flask import abort, request
from .db import is_jwt_valid
from os import getenv, urandom

secret_key = getenv("APP_SECRET_KEY") or urandom(24)

def public_endpoint(function):
    function.is_public = True
    return function

def Generate_JWT(payload: dict):
    import jwt
    encoded_jwt = jwt.encode(payload, secret_key, algorithm="HS256")
    return encoded_jwt
