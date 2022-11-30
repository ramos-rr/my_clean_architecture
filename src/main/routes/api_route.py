from flask import Blueprint, jsonify, request, render_template, make_response
from ..auth_jwt import token_generator, token_verify
from src.main.composer import register_user_composite, register_pet_composite, find_user_composite, find_pet_composite
from src.main.adapter import flask_adapter
from ...presenters.helpers import HttpRequest

api_routes_bp = Blueprint("api_routes", __name__, template_folder='templates')


@api_routes_bp.route('/')
def home():

    menu_list = ["login", "statistics"]
    return render_template('home.html', menu_list=menu_list)


@api_routes_bp.route("/secret", methods=["GET"])
@token_verify
def secret_route(token, exp):

    return jsonify(
        {
            "data": {
                "token_info": {
                    "token": token,
                    "exp": exp
                }
            }
        }
    ), 200


@api_routes_bp.route('/login')
def login():
    return render_template('login.html')


@api_routes_bp.route('/auth', methods=["POST"])
def auth():

    make_response(render_template('login.html'))
    login_entry = request.form.to_dict()

    if "username" in login_entry and "password" in login_entry:
        new_request = HttpRequest(query=login_entry)
        response = flask_adapter(request=new_request, api_route=find_user_composite.find_user_composer())

        if response.status_code == 200:
            if (response.body[0].username == login_entry["username"]) \
                    and (response.body[0].password == login_entry["password"]) and response.body[0].superuser:
                return "<h1>OK! Is a superuser</h1>"
            elif (response.body[0].username == login_entry["username"]) \
                    and (response.body[0].password == login_entry["password"]) and not response.body[0].superuser:
                return "<h1>Almost OK! Is not a superuser</h1>", 401
            else:
                return "<h1>User not allowed. Please verify Username or password</h1>", 401
        else:
            return {"error": "Request denied! User doesn't exist", "status": 403}, 403
    else:
        return {
            "error": "Must inform a username and password"
        }, 403
    token = token_generator.generate(uid=10)
    print(token)
    return jsonify(
        {
            "token": token
        }
    ), 200


@api_routes_bp.route("/api/users", methods=["POST"])
@token_verify
def register_user(token, exp):
    """register user route"""

    message = None
    response = flask_adapter(request=request, api_route=register_user_composite.register_user_composer())
    print(f'Token used: {token}')
    print(f'Minutes to expire: {exp}')
    if response.status_code < 300:
        message = {
            "type": "users",
            "user_id": response.body.id,
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


@api_routes_bp.route("/api/pets", methods=["POST"])
@token_verify
def register_pet(token, exp):
    """register pet route"""

    message = None
    response = flask_adapter(request=request, api_route=register_pet_composite.register_pet_composer())
    print(f'Token used: {token}')
    print(f'Minutes to expire: {exp}')
    if response.status_code < 300:
        message = {
            "type": "pets",
            "pet_id": response.body.id,
            "attributes": {"petname": response.body.petname,
                           "specie": response.body.specie,
                           "age": response.body.age,
                           "register_date": response.body.register_date},
            "relationship": {
                "owner": {
                    "type": "users",
                    "user_id": response.body.user_id
                }
            }
        }

    else:
        return {
            "error": response.body["error"],
            "status": response.status_code,
            "detail": response.body["detail"].message
        }, response.status_code

    return jsonify({"data": message}), response.status_code  # STATUS CODE COMES OUTSIDE


@api_routes_bp.route("/api/users", methods=["GET"])
@token_verify
def find_user(token, exp):
    """find user route"""

    message = None
    response = flask_adapter(request=request, api_route=find_user_composite.find_user_composer())

    pet_found = dict()

    try:
        if len(response.body[1]) != 0:
            for n, p in enumerate(response.body[1], start=1):
                pet_found[f"pet_id_{n}"] = p.id
    except:
        pass

    print(f'Token used: {token}')
    print(f'Minutes to expire: {exp}')
    if response.status_code < 300:
        message = [{
            "type": "users",
            "user_id": response.body[0].id,
            "attributes": {"username": response.body[0].username,
                           "register_date": response.body[0].register_date},
            "relationship": {
                "type": "pets",
                "data": pet_found
            }
        }]

    else:
        return {
            "error": response.body["error"],
            "status": response.status_code,
            "detail": response.body["detail"].message
        }, response.status_code

    return jsonify({"data": message}), response.status_code  # STATUS CODE COMES OUTSIDE


@api_routes_bp.route("/api/pets", methods=["GET"])
@token_verify
def find_pet(token, exp):
    """find pet route"""

    message = list()
    response = flask_adapter(request=request, api_route=find_pet_composite.find_pet_composer())
    print(f'Token used: {token}')
    print(f'Minutes to expire: {exp}')
    if response.status_code < 300:

        for pet in response.body:

            result = {
                "type": "pets",
                "pet_id": pet.id,
                "attributes": {"petname": pet.petname,
                               "specie": pet.specie,
                               "age": pet.age,
                               "register_date": pet.register_date},
                "relationship": {
                    "owner": {
                        "type": "users",
                        "user_id": pet.user_id
                    }
                }
            }
            message.append(result)
    else:
        return {
            "error": response.body["error"],
            "status": response.status_code,
            "detail": response.body["detail"].message
        }, response.status_code

    return jsonify({"data": message}), response.status_code  # STATUS CODE COMES OUTSIDE
