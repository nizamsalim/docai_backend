from flask import Blueprint, request
from ..utils.factory import get_project_service
from ..middleware.protected import protected
from ..schemas.project_schema import CreateProjectSchema
from ..utils.response import ResponseBuilder
import json

project_blueprint = Blueprint("projects", __name__)

service = get_project_service()


@project_blueprint.route("", methods=["POST"])
@protected
def create_project():
    data = CreateProjectSchema(**(request.get_json()))
    res = service.create_project(data)
    return ResponseBuilder.response(res.to_dict(), data_item="project")


@project_blueprint.route("", methods=["GET"])
@protected
def get_all_projects():
    res = service.get_all_projects()
    response_data = []
    for project in res:
        project_dict = project.to_dict()
        del project_dict["sections"]
        response_data.append(project_dict)
    return ResponseBuilder.response(response_data, data_item="projects")


@project_blueprint.route("/<string:project_id>", methods=["GET"])
@protected
def get_project(project_id: str):
    res = service.get_project_data(project_id)
    return ResponseBuilder.response(res.to_dict(), data_item="project")
