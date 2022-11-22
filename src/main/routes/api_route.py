from flask import Blueprint, jsonify, request
from src.main.composer import register_user_composite
from src.main.adapter import flask_adapter


api_routes_bp = Blueprint("api_routes", __name__)


@api_routes_bp.route("/api/users", methods=["POST"])
def register_user():
    """register user route"""

    message = None
    response = flask_adapter(request=request, api_route=register_user_composite.register_user_composer())
    if response.status_code < 300:
        message = {
            "type": "users",
            "id": response.body.id,
            "attributes": {"username": response.body.username,
                           "register_date": response.body.register_date},
        }

    else:
        return {
            "error": response.body["error"],
            "status": response.status_code,
            "detail": response.body["detail"].message
        }, response.status_code

    return jsonify({"data": message}), response.status_code  # STATUS CODE COMES OUTSIDE
