# middleware/auth.py
from functools import wraps
from flask import request, jsonify
import os
from ..utils.jwt import JWTProvider


SECRET_KEY = os.getenv("JWT_SECRET")

def protected(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        access_token = request.cookies.get("access_token")

        payload = JWTProvider.decode_token(access_token) # {id}
        request.user = payload
        

        return fn(*args, **kwargs)
    return wrapper
