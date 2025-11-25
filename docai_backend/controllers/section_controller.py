from flask import Blueprint, request
from ..utils.factory import get_section_service
from ..schemas.section_schema import RefineSectionSchema, UpdateSectionSchema
from ..utils.response import ResponseBuilder
from ..middleware.protected import protected

section_blueprint = Blueprint("sections", __name__)

service = get_section_service()


@section_blueprint.route("/<string:section_id>", methods=["POST"])
@protected
def refine_section_content(section_id: str):
    body = RefineSectionSchema(**(request.get_json()))
    res = service.refine_section(section_id, body)
    return ResponseBuilder.response(res.to_dict(), "section")


@section_blueprint.route("/<string:section_id>", methods=["PUT"])
@protected
def update_section(section_id: str):
    print("flag")
    body = UpdateSectionSchema(**(request.get_json()))
    res = service.update_section(section_id, body)
    return ResponseBuilder.response(res.to_dict(), "section")
