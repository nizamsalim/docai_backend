from flask.blueprints import Blueprint
from flask import request,jsonify
from ..schemas.auth_schema import LoginRequest,RegisterRequest
from ..contracts.user_dto import UserDTO
from ..utils.factory import get_auth_service
from ..utils.response import ResponseBuilder
from pydantic import ValidationError

auth_blueprint = Blueprint("auth",__name__)

service = get_auth_service()

@auth_blueprint.route("/register",methods=["POST"])
def register():
    data = RegisterRequest(**(request.get_json()))
    res,auth_token = service.register_user(data)
    return ResponseBuilder.response(res.to_dict(),auth_token,"user")

@auth_blueprint.route("/login",methods=["POST"])
def login():
    data = LoginRequest(**(request.get_json()))
    res,auth_token = service.login_user(data)
    return ResponseBuilder.response(res.to_dict(),auth_token,"user")

@auth_blueprint.route("/me",methods=["POST"])
def validate():
    access_token = request.cookies.get("access_token")
    res = service.validate_user(access_token)
    return ResponseBuilder.response(res.to_dict(),data_item="user")


