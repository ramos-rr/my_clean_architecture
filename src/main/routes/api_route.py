from flask import Blueprint, jsonify
# from src.main.composer import register_user_composite


api_routes_bp = Blueprint("api_routes", __name__)


@api_routes_bp.route("/api", methods=["GET"])
def something():
    """testing"""

    return jsonify({"Programador": "lhama"})
