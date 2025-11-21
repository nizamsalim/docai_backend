import os
import jwt
from .exception import MissingAccessTokenError,InvalidAccessTokenError
class JWTProvider:
    JWT_SECRET = os.environ.get("JWT_SECRET")

    @staticmethod
    def create_token(user_id:str):
        return jwt.encode({"id":user_id},JWTProvider.JWT_SECRET,algorithm="HS256")
    
    @staticmethod
    def decode_token(access_token:str):
        try:
            if access_token is None:
                raise MissingAccessTokenError()
            payload = jwt.decode(access_token,JWTProvider.JWT_SECRET,algorithms="HS256")
            return payload
        except MissingAccessTokenError:
            raise
        except jwt.InvalidTokenError as e:
            raise InvalidAccessTokenError()
        except Exception as e:
            raise InvalidAccessTokenError()