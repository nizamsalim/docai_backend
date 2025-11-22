from flask.blueprints import Blueprint
from flask import request
from ..schemas.auth_schema import LoginSchema,RegisterSchema
from ..utils.factory import get_auth_service
from ..utils.response import ResponseBuilder

auth_blueprint = Blueprint("auth",__name__)

service = get_auth_service()

@auth_blueprint.route("/register",methods=["POST"])
def register():
    data = RegisterSchema(**(request.get_json()))
    res,auth_token = service.register_user(data)
    return ResponseBuilder.response(res.to_dict(),auth_token,"user")

@auth_blueprint.route("/login",methods=["POST"])
def login():
    data = LoginSchema(**(request.get_json()))
    res,auth_token = service.login_user(data)
    return ResponseBuilder.response(res.to_dict(),auth_token,"user")

@auth_blueprint.route("/logout",methods=["POST"])
def logout():
    return ResponseBuilder.logout()

@auth_blueprint.route("/me",methods=["GET"])
def validate():
    access_token = request.cookies.get("access_token")
    res = service.validate_user(access_token)
    return ResponseBuilder.response(res.to_dict(),data_item="user")


