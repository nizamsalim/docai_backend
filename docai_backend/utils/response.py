from flask import make_response
class ResponseBuilder:
    @staticmethod
    def response(data:dict,auth_token:str):
        response = make_response(data)
        response.set_cookie(
            "access_token",
            auth_token,
            httponly=True,
            secure=True,     # True in production
            samesite="None", 
        )
        return response