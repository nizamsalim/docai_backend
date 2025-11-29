from flask import Blueprint, request
from ..middleware.protected import protected
from ..utils.response import ResponseBuilder
from ..utils.factory import get_refinement_service

refinement_blueprint = Blueprint("refinements", __name__)

service = get_refinement_service()


@refinement_blueprint.route(
    "/<string:refinement_id>/<string:rating>", methods=["PATCH"]
)
@protected
def rate_refinement(refinement_id: str, rating: str):
    res = service.rate_refinement(refinement_id, rating)
    return ResponseBuilder.response(res.to_dict(), "refinement")
