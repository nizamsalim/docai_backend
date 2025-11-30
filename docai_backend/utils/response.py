from flask import make_response, send_file
from io import BytesIO


class ResponseBuilder:
    @staticmethod
    def auth_response(data: dict, auth_token: str = None, data_item: str = "data"):
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
    def response(data: dict | list | str, data_item: str):
        res = make_response({"success": True, data_item: data})
        return res

    @staticmethod
    def file(buffer: BytesIO, project_title: str, project_type: str):
        mime_type = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            if project_type == "docx"
            else ""
        )
        return send_file(
            buffer,
            mimetype=mime_type,
            download_name=f"{project_title}.docx",
            as_attachment=True,
        )

    @staticmethod
    def logout():
        response = make_response({"success": True})
        response.delete_cookie(
            "access_token", httponly=True, secure=True, samesite="None"
        )
        return response
