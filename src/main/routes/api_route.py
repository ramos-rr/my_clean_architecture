from flask import Blueprint, jsonify, request
import jwt
from datetime import datetime, timedelta
# from src.main.composer import register_user_composite, register_pet_composite, find_user_composite, find_pet_composite
# from src.main.adapter import flask_adapter


api_routes_bp = Blueprint("api_routes", __name__)


@api_routes_bp.route("/secret", methods=["GET"])
def secret_route():
    raw_token = request.headers.get("Authorization")

    if not raw_token:
        return jsonify(
            {
                "error": "Not allowed"
            }), 401
    # Let's arrive here
    try:
        if raw_token.count(" ") == 1:
            token = raw_token.split()[1]
        else:
            token = raw_token

        token_info = jwt.decode(token, key="1234", algorithms="HS256")

    except jwt.ExpiredSignatureError:
        return jsonify(
            {
                "error": "Token expired"
            }
        ), 401
    except jwt.InvalidTokenError:
        return jsonify(
            {
                "error": "Invalid token"
            }
        ), 401
    else:
        return jsonify(
            {
                "data": "secret message",
                "token expiration": token_info["exp"]
            }
        )


@api_routes_bp.route('/auth', methods=["POST"])
def authorization_route():

    token = jwt.encode(
        {
            "exp": datetime.utcnow() + timedelta(seconds=1)
        },
        key='1234',
        algorithm="HS256"
    )
    print(token)
    return jsonify(
        {
            "token": token
        }
    ), 200

# @api_routes_bp.route("/api/users", methods=["POST"])
# def register_user():
#     """register user route"""
#
#     message = None
#     response = flask_adapter(request=request, api_route=register_user_composite.register_user_composer())
#     if response.status_code < 300:
#         message = {
#             "type": "users",
#             "user_id": response.body.id,
#             "attributes": {"username": response.body.username,
#                            "register_date": response.body.register_date},
#         }
#
#     else:
#         return {
#             "error": response.body["error"],
#             "status": response.status_code,
#             "detail": response.body["detail"].message
#         }, response.status_code
#
#     return jsonify({"data": message}), response.status_code  # STATUS CODE COMES OUTSIDE
#
#
# @api_routes_bp.route("/api/pets", methods=["POST"])
# def register_pet():
#     """register pet route"""
#
#     message = None
#     response = flask_adapter(request=request, api_route=register_pet_composite.register_pet_composer())
#     if response.status_code < 300:
#         message = {
#             "type": "pets",
#             "pet_id": response.body.id,
#             "attributes": {"petname": response.body.petname,
#                            "specie": response.body.specie,
#                            "age": response.body.age,
#                            "register_date": response.body.register_date},
#             "relationship": {
#                 "owner": {
#                     "type": "users",
#                     "user_id": response.body.user_id
#                 }
#             }
#         }
#
#     else:
#         return {
#             "error": response.body["error"],
#             "status": response.status_code,
#             "detail": response.body["detail"].message
#         }, response.status_code
#
#     return jsonify({"data": message}), response.status_code  # STATUS CODE COMES OUTSIDE
#
#
# @api_routes_bp.route("/api/users", methods=["GET"])
# def find_user():
#     """find user route"""
#
#     message = None
#     response = flask_adapter(request=request, api_route=find_user_composite.find_user_composer())
#     if response.status_code < 300:
#         message = [{
#             "type": "users",
#             "user_id": response.body[0].id,
#             "attributes": {"username": response.body[0].username,
#                            "register_date": response.body[0].register_date},
#         }]
#
#     else:
#         return {
#             "error": response.body["error"],
#             "status": response.status_code,
#             "detail": response.body["detail"].message
#         }, response.status_code
#
#     return jsonify({"data": message}), response.status_code  # STATUS CODE COMES OUTSIDE
#
#
# @api_routes_bp.route("/api/pets", methods=["GET"])
# def find_pet():
#     """find pet route"""
#
#     message = list()
#     response = flask_adapter(request=request, api_route=find_pet_composite.find_pet_composer())
#     if response.status_code < 300:
#
#         for pet in response.body:
#
#             result = {
#                 "type": "pets",
#                 "pet_id": pet.id,
#                 "attributes": {"petname": pet.petname,
#                                "specie": pet.specie,
#                                "age": pet.age,
#                                "register_date": pet.register_date},
#                 "relationship": {
#                     "owner": {
#                         "type": "users",
#                         "user_id": pet.user_id
#                     }
#                 }
#             }
#             message.append(result)
#     else:
#         return {
#             "error": response.body["error"],
#             "status": response.status_code,
#             "detail": response.body["detail"].message
#         }, response.status_code
#
#     return jsonify({"data": message}), response.status_code  # STATUS CODE COMES OUTSIDE
