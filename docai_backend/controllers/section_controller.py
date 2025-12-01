from flask import Blueprint, request
from ..utils.factory import get_section_service
from ..schemas.section_schema import (
    RefineSectionSchema,
    UpdateSectionSchema,
    CommentSchema,
)
from ..utils.response import ResponseBuilder
from ..middleware.protected import protected

section_blueprint = Blueprint("sections", __name__)

service = get_section_service()


@section_blueprint.route("/<string:section_id>/refinements", methods=["POST"])
@protected
def refine_section_content(section_id: str):
    body = RefineSectionSchema(**(request.get_json()))
    print(body.model_name)
    res = service.refine_section(section_id, body)
    return ResponseBuilder.response(res.to_dict(), "section")  # return only refinement


@section_blueprint.route("/<string:section_id>", methods=["PUT"])
@protected
def update_section(section_id: str):
    body = UpdateSectionSchema(**(request.get_json()))
    res = service.update_section(section_id, body)
    return ResponseBuilder.response(res.to_dict(), "section")


@section_blueprint.route("/<string:section_id>/comments", methods=["POST"])
@protected
def comment_section(section_id: str):
    body = CommentSchema(**(request.get_json()))
    res = service.add_section_comment(section_id, body)
    return ResponseBuilder.response(res, "comment")


@section_blueprint.route(
    "/<string:section_id>/comments/<string:comment_id>", methods=["PUT"]
)
@protected
def update_comment(section_id: str, comment_id: str):
    body = CommentSchema(**(request.get_json()))
    res = service.update_section_comment(section_id, comment_id, body)
    return ResponseBuilder.response(res, "comment")


@section_blueprint.route(
    "/<string:section_id>/comments/<string:comment_id>", methods=["DELETE"]
)
@protected
def delete_comment(section_id: str, comment_id: str):
    res = service.delete_section_comment(section_id, comment_id)
    return ResponseBuilder.response(res, "comment")


@section_blueprint.route(
    "/<string:section_id>/regenerate/<string:model_name>", methods=["GET"]
)
@protected
def regenerate_section(section_id: str, model_name: str):
    res = service.regenerate_section_content(section_id, model_name)
    return ResponseBuilder.response(res.to_dict(), "section")
