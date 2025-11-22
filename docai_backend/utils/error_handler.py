from ..utils.exception import BaseAppException
from pydantic import ValidationError as PydanticValidationError
from flask import jsonify

def register_error_handlers(app):

    @app.errorhandler(BaseAppException)
    def handle_custom_exceptions(error):
        response = {
            "success": False,
            "message": error.message,
            "error": error.data,
            "errorCode":error.error_code,
            "statusCode":error.status_code
        }
        if response["error"] == {}:
            del response["error"]
        return jsonify(response), error.status_code
    
    @app.errorhandler(PydanticValidationError)
    def handle_pydantic_exceptions(error):
        locs = []
        for err in error.errors():
            if err["type"] == "missing":
                locs.append(err["loc"][0])
        e = [{"field":loc,"message":f"{loc} is a required field"} for loc in locs]
        response = {
            "success": False,
            "message": "Input validation failed",
            "error": e,
            "errorCode":"VALIDATION_ERROR",
            "statusCode":422
        }
        return jsonify(response), 422
