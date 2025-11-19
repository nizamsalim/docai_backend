import os
import jwt
class JWTProvider:
    JWT_SECRET = os.environ.get("JWT_SECRET")

    @staticmethod
    def create_token(user_id:str):
        return jwt.encode({"id":user_id},JWTProvider.JWT_SECRET,algorithm="HS256")