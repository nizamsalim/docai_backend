from flask import make_response


class ResponseBuilder:
    @staticmethod
    def response(data: dict | list, auth_token: str = None, data_item: str = "data"):
        response = make_response({"success": True, data_item: data})
        if auth_token:
            response.set_cookie(
                "access_token",
                auth_token,
                httponly=True,
                secure=True,  # True in production
                samesite="None",
            )
        return response

    @staticmethod
    def logout():
        response = make_response({"success": True})
        response.delete_cookie(
            "access_token", httponly=True, secure=True, samesite="None"
        )
        return response
