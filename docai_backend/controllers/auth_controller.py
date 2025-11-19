from flask.blueprints import Blueprint
from flask import request,jsonify
from ..schemas.auth_schema import LoginRequest,RegisterRequest
from ..contracts.user_dto import UserDTO
from ..utils.factory import get_auth_service
from ..utils.response import ResponseBuilder
from pydantic import ValidationError

auth_blueprint = Blueprint("auth",__name__,url_prefix="/auth")

service = get_auth_service()

@auth_blueprint.route("/register",methods=["POST"])
def register():
    data = RegisterRequest(**(request.get_json()))
    res,auth_token = service.register_user(data)
    return ResponseBuilder.response(res.to_dict(),auth_token)

@auth_blueprint.route("/login",methods=["POST"])
def login():
    data = LoginRequest(**(request.get_json()))
    res,auth_token = service.login_user(data)
    return ResponseBuilder.response(res.to_dict(),auth_token)

