from flask import Blueprint, request
from ..utils.factory import get_section_service
from ..schemas.section_schema import RefineSectionSchema

section_blueprint = Blueprint("sections", __name__)

service = get_section_service()


@section_blueprint.route("/<string:section_id>", methods=["POST"])
def refine_section_content(section_id: str):
    body = RefineSectionSchema(**(request.get_json()))
    res = service.refine_section(section_id, body)
