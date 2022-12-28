from flask import Blueprint, jsonify, request, render_template, make_response, redirect, url_for
from ..auth_jwt import token_generator, token_verify, active_token
from src.main.composer import register_user_composite, register_pet_composite, find_user_composite, find_pet_composite
from src.main.adapter import flask_adapter
from ...presenters.helpers import HttpRequest
from src.infra.config import DbConnectionHandler
from src.infra.entities import Users

api_routes_bp = Blueprint("api_routes", __name__, template_folder='templates')


@api_routes_bp.route('/')
def index():

    menu_list = ["login", "statistics"]
    return render_template('index.html', menu_list=menu_list)


@api_routes_bp.route("/home", methods=["GET", "POST"])
@token_verify
def home(token, exp, username):
    conn = DbConnectionHandler().__enter__()
    query = conn.session.query(Users).all()
    conn.session.close()
    users = list()
    for q in query:
        user = dict()
        request_user = HttpRequest(query={"user_id": q.id})
        response = flask_adapter(request=request_user, api_route=find_user_composite.find_user_composer())
        user["id"] = response.body[0].id
        user["username"] = response.body[0].username
        user["pet"] = len(response.body[1])
        users.append(user)
    return render_template('home.html', name=username.title(), users=users), 200


@api_routes_bp.route("/secret", methods=["GET"])
@token_verify
def secret_route(token, exp, username):

    return jsonify(
        {
            "data": {
                "token_info": {
                    "token": token,
                    "exp": exp,
                    "username": username
                }
            }
        }
    ), 200


@api_routes_bp.route('/login')
def login():
    active = active_token.get_token()
    token = active.get('token', None)
    if token is None:
        return render_template('login.html')
    else:
        return redirect(url_for('api_routes.home'), 302)


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
                uid = int(response.body[0].id)
                token = token_generator.generate(uid=uid)
                active_token.fix_token(new_token=token, new_uid=uid, username=login_entry["username"])

                return redirect(url_for('api_routes.home'), 302)

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


@api_routes_bp.route("/register_user", methods=["GET", "POST"])
@token_verify
def register_user(token, exp, username):
    """register user route"""
    if request.method == "POST":
        entry = request.form.to_dict()
        http_request_new_user = HttpRequest(body=entry)
        message = None
        response = flask_adapter(request=http_request_new_user,
                                 api_route=register_user_composite.register_user_composer())
        if response.status_code < 300:
            message = {
                "status": "success",
                "data": {
                    "type": "register users",
                    "user_id": response.body.id,
                    "attributes": {"username": response.body.username,
                                   "register_date": response.body.register_date},
                }
            }
            print(message)
            return redirect(url_for('api_routes.view', user_id=response.body.id), 302)
        else:
            return {
                "error": response.body["error"],
                "status": response.status_code,
                "detail": response.body["detail"].message
            }, response.status_code
    return render_template('register_user.html')


@api_routes_bp.route("/user_<int:user_id>/register_pet", methods=["GET", "POST"])
@token_verify
def register_pet(token, exp, username, user_id):
    """register pet route"""
    conn = DbConnectionHandler().__enter__()
    user = conn.session.query(Users).filter_by(id=user_id).one()
    if request.method == "POST":
        pet_attrib = request.form.to_dict()
        pet_attrib["user_id"] = user_id
        http_request = HttpRequest(body=pet_attrib)
        message = None
        response = flask_adapter(request=http_request, api_route=register_pet_composite.register_pet_composer())
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
            print(message)
            return redirect(url_for("api_routes.view", user_id=user.id), 302)
        elif response.status_code > 300:
            return {"error": response.body["error"], "status": response.status_code,
                    "detail": response.body["detail"].message}, response.status_code
    return render_template('register_pet.html', username=user.username, user_id=user.id)


@api_routes_bp.route("/users", methods=["GET"])
@token_verify
def find_user(token, exp, username):
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


@api_routes_bp.route("/pets", methods=["GET"])
@token_verify
def find_pet(token, exp, username):
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


@api_routes_bp.route('/view/user_<int:user_id>')
@token_verify
def view(token, exp, username, user_id):

    # Get info from users
    http_request_user = HttpRequest(query={"user_id": user_id})
    response_user = flask_adapter(request=http_request_user, api_route=find_user_composite.find_user_composer())

    # Get info from pets
    http_request_pet = HttpRequest(query={"user_id": user_id})
    response_pet = flask_adapter(request=http_request_pet, api_route=find_pet_composite.find_pet_composer())

    # Compose query
    user = response_user.body[0]
    pets = None
    if len(response_user.body[1]) > 0:
        pets = response_pet.body

    return render_template('view_user.html', username=user.username.title(), user_id=user_id, pets=pets)


@api_routes_bp.route('/delete/user_<int:user_id>', methods=["GET", "POST"])
@token_verify
def delete_user(token, exp, username, user_id):
    # if request.method == "POST":
    conn = DbConnectionHandler().__enter__()
    user = conn.session.query(Users).filter_by(id=user_id).one()
    conn.session.delete(user)
    conn.session.commit()
    print({"status": "success", "body": {
        "type": "users",
        "operation": "DELETE USER FROM DATABASE",
        "data": {"user_id": user_id, "username": user.username}}})
    conn.session.close()
    return redirect(url_for('api_routes.home'), 302)


@api_routes_bp.route('/edit/user_<int:user_id>', methods=["GET", "POST"])
@token_verify
def edit_user(token, exp, username, user_id):
    conn = DbConnectionHandler().__enter__()
    user = conn.session.query(Users).filter_by(id=user_id).one()
    if request.method == "POST":
        new_data = {"username": request.form.get("username"), "password": request.form.get("password")}
        if new_data["username"] != '':
            user.username = new_data["username"]
            conn.session.commit()
        if new_data["password"] != '':
            user.password = new_data["password"]
            conn.session.commit()
        conn.session.close()
        print({
            "status": "success",
            "data": {
                "type": "edit user",
                "user_id": user_id,
                "username": new_data["username"]
            }
        })
        return redirect(url_for('api_routes.home'), 302)
    conn.session.close()
    return render_template('edit_user.html', username=user.username, user_id=user.id)


@api_routes_bp.route('/logout')
@token_verify
def logout(token, exp, username):
    active_token._logout()
    token_generator._logout()
    print({"status": "success", "data": {"type": "logout", "username": username, "token": token}})
    return redirect(url_for('api_routes.login'), 302)
