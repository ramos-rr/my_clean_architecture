 # my_clean_architecture
Repository based on the Clean Architecture book from Robert C Martin and YouTube classes from "programador Lhama"<br>
#### What to expect:
This course has the objectve to develop a full app to manage USERS and PETS, all the way from a SQL database storage 
data to the interaction with the exterior. Therefore, we must apply all CLEAN ARCHITECTURE concepts.<br>
<br>
#### DON'T FORGET TO SET UP THE VISTUAL ENVIRONMENT AND CREATE .ENV FILE !<br>
- Use PIPENV to 
- If you are going to fork this repository, do not forget to create a `.env` file in project's root by copying the 
content in `contrib/env-sample` (you can copy, paste and rename it).

## Check YouTube channel ["Programador Lhama"](https://www.youtube.com/watch?v=YAMgtR3aCuY&list=PLAgbpJQADBGJmTxeRZKWvdJAoJj8_x3si&index=1)
### Remember that _clean architecture_ basically follow the scheme below:
<img src="images/clean_architecture.jpg" alt="clean_architecture" width="480" height=""><br>
Author's explanation of the picture: _"The concentric circles in (above) figure represents areas of software. In general,
the further in you go, the higher level the software becomes. The outer circles are mechanisms. The inner circles are
polices."_<br>
_"Nothing in an inner cicle can know anything at all about something in an outer cicle. In particular, the name of 
<b>something declared in an outer cicle must not be mentioned by any code in an inner cicle</b>. That includes functions
, classes, variables, or any other named software entity"_ p.203<br><br>

#### <b>ENTERPRISE BUSINESS RULES:</b>
Object with method, a set of data structures or function that <b> _can be used_</b>
by many different application.<br>
<b> - Expect not to ever change</b>, except some eventual minor ajustments<br><br>

#### <b>APPLICATION BUSINESS RULES (USE CASES):</b>
Features that orchestrate the flow of data to and from those entities. In general, they do what users want to obtain
by using the software.<br>
<b> - Do not expect changes in this layer to affect _entities_</b><br>
<b> - Also we do not expect the changes in database or UI (dealt by entities) to affect this USE CASE layer.</b><br><br>

#### <b>INTERFACE ADAPTERS:</b>
Convert datas from use cases language to external and convenient languages, such as WEB agencies (e.g. http request in 
REST format). Overall, this layer is implemented to transform external data to internal format data, that allow use 
case and entities to undestand, and then, return to exterior whatever data it has got from inner software within the
most convenient format needed by outer services.<br>
<b> - Expect that no code inward of this layer to deal with any database</b><br><br>

#### <b>FRAMEWORK & DRIVERS:</b>
This outermost layer is where frameworks and tools, such as database and web frameworks, find themselves. It may have 
little amount of code here, thus it might glue code that communicates with inner circles.<br>
<b> - Expect frequent changes to this layer.</b><br><br>

## ENTITIES
## Relation between classes<br>
<img src="images/relacao_usuario_pets.png" alt="relationship_classes" width="480" height=""><br>
- A User takes care of some Pets<br>
### Diagram of a spcific classe<br>
<img src="images/diagram_class.png" alt="class_diagram" width="300" height=""><br>
- Shows how a Class should behave to relate with other classes (Methods and Attributes)<br>
1. We've started setting up the `infra` to store our DB. For this project, we will just use sqlite throught sqlalchemy<br>
- CREATE: `infra/config/db_config.py`
- CREATE: `<db/config.py> class DbConnectionHandler` and follow the image 2.<br>
- CREATE: `infra/config/db_base.py` to tell sqlalchemy what is going to be inside DB and their relationship between them<br>
- CREATE: `<db_config.py> Base = declarative_base()` '(_from sqlalchemy.ext.declarative import declarative_base_)'.
This to awake DB.<br>
- EDIT: `<config/__init__.py>` and point what to export > `from .db_base import Base` and `from .db_config_py import 
DbConnectionHandler`<br><br>

- CREATE: `infra/entities/` to stablish the TABLE for the DB<br>
- CREATE: `infra/entities/pets.py` and `infra/entities/users.py` that are going to be the main actors in this project<br>
- CREATE: `<users.py> class Users(Base)`, importing Base from our `config`, and also import TABLE features from sqlalchemy,
such as Column, String, Integer<br>
- CREATE: `<pets.py> class Pets(Base)`, importing Base from our `config`, and also import TABLE features from sqlalchemy,
such as Column, String, Integer<br>
- EDIT: `<entities/__init__.py>` and point what to export > `from .pets import Pets` and `from .users import Users`<br><br>

- RUN TERMINAL:<br>
`$ python`<br> `>>> from src.infra.config import *` <br>`>>> from src.infra.entities import *` <br>
`# CHECK IF EVERYTHING HAS BEEN INSTATIATED`<br>
`>>> Base` <br> `<class 'sqlalchemy.orm.decl_api.Base'>` <br>
`>>> DbConnectionHandler` <br> `<class 'src.infra.config.db_config_py.DbConnectionHandler'>` <br>
`>>> Users`<br>`<class 'src.infra.entities.users.Users'>`<br>
`>>> Pets`<br>`<class 'src.infra.entities.pets.Pets'>`<br>
`# EVERYTHING SEEMS TO BE FINE. CONTINUING...`<br>
` >>> db_conn = DbConnectionHandler()`<br>
`# CHECK OBJECT DB_CONN`<br>
`>>> db_conn` <br> `<src.infra.config.db_config_py.DbConnectionHandler object at 0x000001FC4303F730>`<br>
`# CALL ENGINE TO PUT PARTS TOGETHER`<br>
`>>> engine = db_conn.get_engine()`<br> `>>> engine`<br> 
`Engine(sqlite:///storage.db)`<br>
`# COMMAND THE CREATION OF THE FILE SQLITE DB`<br>
`>>> Base.metadata.create_all(engine)`<br>
<br>

- SEE: `storage.db` must have been created in your project's root

### TIP to create and manage DB FROM SQLALCHEMY:<br>
1. When stablishing a connection, you have to set up a ENGINE:<br>
2. Define a SESSION, which is NONE initially, but recieves a value after started<br>
3. Define _ _ enter _ _() and _ _ exit _ _() methods to set up a session every time the class 
is called, ado close in the end
<br>

```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DbConnectionHandler:

    def __init__(self):
        self.__connection_string = "sqlite:///storage.db"  # This string is need by sqlalchemy
        self.session = None

    def get_engine(self):
        """
        Create a connection to DB
        :return: connection engine
        """
        engine = create_engine(self.__connection_string)
        return engine

    # Define a method to enter DB to garantee some levels of security
    def __enter__(self):
        engine = create_engine(self.__connection_string)
        session_maker = sessionmaker()
        self.session = session_maker(bind=engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
```
<br>

5. Finally, when introducing new data in DB, call `session` and one of this four commands:
- <connection_name>.session.add( <new_data> )<br>
- <connection_name>.session.commit()<br>
- <connection_name>.session.rollback()<br>
- <connection_name>.session.close()<br>
- OBS: generally, this features are used with <b>try / finally</b> resource<br>
<br>
## CREATING A USERREPOSITORY AND PETREPOSITORY CLASS<br>
<img src="images/user_repository_diagram.png" alt="user_repository_diagram" width="400" height=""><br>
- Now it is time to set up a USER REPOSITORY and a PET REPOSITORY CLASS that will call both entities and
database as desired

## THE FULL PICTURE - DEVELPMENT DIAGRAM<br>
<img src="images/models_and_repository_diagram.png" alt="models_and_repository_diagram" width="650" height=""><br>

## USECASE FOR USER AND PET
<img src="images/usecase_diagram.png" alt="usecase_diagram" width="550" height=""><br>
- ACTOR: Our user. He can performe all this actions described in the diagram;<br>
- ACTIONS: Generic descriptions of all possible interaction allowed for this actor;<br>
- INCLUDE : A small dependency brought by diagram telling that a User must be related to a Pet everytime;<br>
- BY METHODS : List of required information to perform a database query.<br>
In the end, use case diagram followed as this:<br>
<img src="images/use_case_diagram.png" alt="use_case_diagram" width="750" height=""><br>
<_see it better in `.dia` file_><br>

## CONTROLLER DIAGRAM
Remember that this project is becoming wide, thus it's impossible to bring the full diagram picture that is readable.
For now on, we'll provide only fraction of it.
<img src="images/controller_diagram.png" alt="controller_diagram" width="550" height=""><br>
<br>

## EXTERNAL INTERFACES - LAST LAYER<br>
- For this final layer of development, we have to put all peaces together<br>
- For user interaction, we'll use FLASK framework</b><br>
- We'll also implement `DEBUG=True` to help us track down all errors.<br>
<br>

### COMPOSERS<br>
Inward composers' layer, it is time set up features that connect different layres in order to proper run the 
software<br>
<img src="images/project-layers-table.png" alt="project-layers" width="450" height=""><br>
_See above how this project looks like so far. Now let's connect all pieces together_<br><br>

#### CREATE A COMPOSER<br>
- Instatiate all part together, like example below:
```
from src.presenters.interface import RouteInterface
from src.presenters.controllers import RegisterUserController
from src.data.register_user import RegisterUser
from src.infra.repo import UserRepository


def register_user_composer() -> RouteInterface:
    """
    Function to compose register user
    :param: None
    :return: Object with register user route
    """

    user_repo = UserRepository()
    register_user_usecase = RegisterUser(user_repository=user_repo)
    register_user_route = RegisterUserController(register_user_usecase=register_user_usecase)

    return register_user_route
    
```
<br>



#### FLASK IT -> `SRC/MAIN/CONFIGS`
- Start installing FLASK: `$ pipenv install Flask`. Like all web framework, you must set up an APP to begin with<br>
- CREATE `app.py` in src/main/configs;<br>
- IMPORT `from flask import Flask`;<br>
- INSTALL `Flask-Cors`: `pipenv install Flask-Cors` to give some treatments for us.;<br>.
- CONFIG APP. Name it whatever you want. It's going to be `app` for this tutorial :<br>

```
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
```
<br>

- EXPORT `app` in `__init__.py`

#### ROUTE YOUR COMPOSER<br>
- Create `api_router.py` in src/main/routes;<br>
- IMPORT BLUEPRINT -> Flask works basically with BluePrints: `from flask import Blueprint`
- SET UP a function to return something when called. <b>Don't forget to use a decorator</b> to guid flask
right in the function. When doing so, insert the METHOD desired. In this case, we'll use GET:

```
from flask import Blueprint, jsonify
from src.main.composer import register_user_composite


api_routes_bp = Blueprint("api_routes", __name__)


@api_routes_bp.route("/api", methods=["GET"])
def something():
    """testing"""

    return jsonify({"Programador": "lhama"})
```
<br>

- EXPORT `api=routes_bp` blueprint in `__init__.py`: `from .api_route import api_routes_bp`<br>
- FINISH CONFIGS:<br>
  - IMPORT api_routes_bp from src/main/routes: `from src.main.routes import api_routes_bp`<br>
  - ADD NEW LINE TO <b>REGISTER YOUR BLUEPRINT IN APP</b>: `app.register_blueprint(blueprint=api_routes_bp)`<br>
  <br>

#### RUN
- CREATE `run.py` in project's root;<br>
- IMPORT `app` from src/main/configs: `from src.main.configs import app`<br>
- CONFIG RUN.PY:<br>

```
from src.main.configs import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

```
<br>

- RUN `$python run.py`<br>

## FINALLY ONLINE<br>
- Verify in terminal if FLASK is getting your route: `$ flask routes`:<br>
<img src="images/flask-routes-info.png" alt="flask-routes-info" width="750" height=""><br>
<br>
- Check whether our API is working:<br>
1. See if the terminal has returned a positive message that you are online locally:<br>
<img src="images/flask-online-message.png" alt="flask-online-message" width="650" height=""><br>
2. Go to the browser and type the address showed in terminal. <b> REMEMBER:</b> DON'T FORGET TO FILL REST OF THE URL 
WITH DE ADDRESS YOU ASSIGNED IN ROUTES. In this case, we have `/api`.<br>
<img src="images/browser_url_api_address.png" alt="url_route_api" width="200" height=""><br>
3. Verify in the browser if you get your message (written in api_route) and in the terminal the navegation log:<br>
<img src="images/first_message_online.png" alt="first_message_online" width="280" height=""><br>
<br>
<img src="images/server_log_status_200.png" alt="flask_server_log_status_200" width="600" height=""><br>
<br>

### SET UP ADAPTERS<br>
- Adapters will server to call our composer into routes;<br>
- Adapter parameter will be:<br>
  - <b>HTTP REQUEST:</b> the BODY, QUERY or HEADER that comes from the BROWSER<br>
  - <b>ROUTE:</b> the route inward of the back-end that will recieve and return the request as a RESPONSE<br>

```
from typing import Type
from src.presenters.interface import RouteInterface as Route
from src.presenters.helpers import HttpRequest


def flask_adapter(request: any, api_route: Type[Route]) -> any:
    """
    Adapter patterns to flask
    :param request: Flask Request
    :param api_route: Composite route
    return: Any
    """

    http_request = HttpRequest(body=request.json)
    response = api_route.route(http_request=http_request)

    return response
```

<br>

### UPDATE ROUTE API TO PROCESS RESPONSE<br>
- Now, it's time to call our adapter in ROUTE to expect a Response from it. For this example, we'll use Register User
use case<br>

```
from flask import Blueprint, jsonify, request
from src.main.composer import register_user_composite
from src.main.adapter import flask_adapter  # Here we import our adapter


api_routes_bp = Blueprint("api_routes", __name__)


@api_routes_bp.route("/api/users", methods=["POST"])
def register_user():
    """register user route"""

    message = None
    
    # Here we call the adapter sending out as parameter the HTTP content we got online
    response = flask_adapter(request=request, api_route=register_user_composite.register_user_composer())
    
    # Check if we have a positive response (with data)
    if response.status_code < 300:
        message = {
            "type": "users",
            "id": response.body.id,
            "attributes": {"username": response.body.username,
                           "register_date": response.body.register_date},
        }
    
    # If we got an error, it's time to show which error is that
    else:
        return {
            "error": response.body["error"],
            "status": response.status_code,
            "detail": response.body["detail"].message
        }, response.status_code

    return jsonify({"data": message}), response.status_code  # STATUS CODE COMES OUTSIDE
```
<br>

### REFRESH THE SERVER AND RUN IT AGAIN<br>
- Wait until flask og online;<br>
- OPEN Postman, type the url address, as it is described in `api_route.py`. See the decorator:<br>
`@api_routes_bp.route("/api/users", methods=["POST"])`<br>
- Create a NEW HEADER in POSTMAN for JSON body be well interpreted, in addition to all other autogenerated headres:<br>
  - <b>KEY: `Content-Type`</b><br>
  - <b>VALUE: `application/json`</b><br>
<img src="images/postman-header-json.png" alt="postman-header-json" width="450" height=""><br>

- Create a BODY in POSTMAN in json format:<br>
<img src="images/postman-body-register-user.png" alt="postman-body-register-user" width="600" height=""><br>
<br>
- <strong>SUBMIT :</strong> CHECK THE RESPONSE BODY AND ITS STATUS:<br>
<img src="images/postman-register-user-response-200.png" alt="postman-register-user-response-200" width="600" height="">
<br>

### ERRORS<br>
All errors, casual or intentional, should be addressed. Let us see how and ERROR might appear:<br>
<img src="images/postman-register-user-response-422.png" alt="postman-register-user-response-422" width="650" height="">
<br>
- Remember that all errors related to DataBase is managed in the infrastructure level!<br>
- For, back to `api_route.py` and DEBUG your app if you are not getting it<br>

### FINISHING ALL OTHER COMPOSERS
- Now, we shall finish the set-up for all others composers to adhere our use case diagram. Remember:<br>
  - Register User (arlready in place);<br>
  - Find User;<br>
  - Register Pet;<br>
  - Find Pet.<br>
- For each one of this, a single composite and a different route is necessary.<br>
<br>

## USER VALIDATION - PyJWT<br>
- In order to protect data, we'll aplly a user validation to give access only for authorized users.<br>
- Install PyJWT: `$ pipenv install PyJWT`;<br>
<br>
- Create a TOKEN route:<br>

```
from flask import Blueprint, jsonify, request
import jwt
from datetime import datetime, timedelta

@api_routes_bp.route('/auth', methods=["POST"])
def authorization_route():

    token = jwt.encode(
        {
            "exp": datetime.utcnow() + timedelta(minutes=20)
        },
        key='1234',
        algorithm="HS256"
    )
    return jsonify(
        {
            "token": token
        }
    ), 200
```
<br>

- Parameters used:<br>
  - <b>"exp"</b> = Token expiration time. In this case, we've used 20 minutes;<br>
  - <b>key</b> = Secret key to decode it later;<br>
  - <b>algorithm</b> = Type of algorith that allow adm to track which User used it. To kwon more, check [online](https://stackoverflow.com/questions/39239051/rs256-vs-hs256-whats-the-difference);<br>
<br>
- Launch server and get the token: url = `127.0.0.1:8000/auth`<br>
<img src="images/jwt-token.png" alt="jwt-token" width="" height=""><br>
<br>
<strong>JWT'S TOKENS ARE GENERATED AND STORAGED ONLINE. YOU CAN GENERATE AS MANY TOKENS AS YOU WANT BECAUSE THEY WILL EXPIRE ACCORDING TO YOUR SET UP.</strong><br>
<br>
- Create a secret route to test token:<br>

```
@api_routes_bp.route("/secret", methods=["GET"])
def secret_route():

    raw_token = request.headers.get("Authorization")

    if not raw_token:
        return jsonify(
            {
                "error": "Not allowed"
            }
        ), 401
        
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
                "token_expiration": token_info["exp"]
            }
        ), 200
```
<br>

- Parameters used:
  - `raw_token = request.headers.get("Authorization")` = Go to headers and check if any token has been provided;<br>
  - `if not raw_token` = If no "Authorization" headers exists, than the response will be an error;<br>
  - `if raw_token.count(" ") == 1:` = In case raw token comes with a SPACE character, we split it to get onlu raw token;<br>
  - `token_info = jwt.decode(token, key="1234", algorithms="HS256")` = To decode the token and get its information, such
  as expiration time. Need to enter the very same values from the token generation above;<br>
  - `exceptions` = Treat each exception according to their occurrence. Let's have these two for now;<br>
<br>

- RUN Server and try to get a 200 status code:
<img src="images/jwt-authorization-200.png" alt="jwt-authorization_200" width="" height=""><br>
- TRY ERRORS:<br>
  - Tokenless<br>
  <img src="images/jwt-authorization-no-token.png" alt="jwt-authorization-no-token" width="" height=""><br>
  - Wrong token<br>
  <img src="images/jwt-authorization-invalid-token.png" alt="jwt-authorization-invalid-token" width="" height=""><br>
  - Expired token (set "exp" to 1 seconds, generate another token and use here)<br>
  <img src="images/jwt-authorization-token-expired.png" alt="jwt-authorization-token-expired" width="" height=""><br>
<br>

## FINAL SET UP<br>

### PUT A DECORATOR IN PLACE<br>
- Now, it is time to put this authorization as a decorator to be called before ROUTE process its program;<br>
- CREATE a new package folder: `/src/main/auth_jwt`;<br>
- CREATE a new package folder: `/src/main/auth_jwt/token_handler`;<br>
- CREATE a new file: `token_generator.py`;<br>
- Set UP a new TokenGenerator class:<br>
  - Attributes: token_key, expiration_time, refresh_time;<br>
  - Public Methods: generate_toke(param: user_id), refresh_token(param: token)<br>
  - Private Methods: encode_token(param: user_id)<br><br>

- CREATE a new file: `token_sigleton.py` to make sure that no more than ONE token generator is instantiated in the same
session:<br>

```
from decouple import config
from .token_generator import TokenGenerator
token_generator = TokenGenerator(
    token_key=config("TOKEN_KEY"),
    exp_time_min=config("TOKEN_EXPIRATION_MIN", cast=int),
    refresh_time_min=config("TOKEN_REFRESH_MIN", cast=int)
)
```
<br>

<b>Don't forget to export only this variable outside</b> in `/src/main/auth_jwt/token_handler__init__.py`. This way, 
no body will have access to token generator;<br>
- Back to `/src/main/auth_jwt`, create a new file `token_verifier.py`;<br><br>

- <b>NOW, TIME TO SET UP DECORATOR;</b><br>
  - CREATE a callable function: `def token_verify(function: callable) -> callable:`
  - Insede this function, create another function and name it _decorated()_: `def decorated(*args, **kwargs):`;<br>
    - <b>*args:</b> Obligatory parameter when creating a decorator that inherits the class who has called it;<br>
    - <b>*kwargs:</b> Obligatory parameter when creating a decorator that inherits the class who has called it;<br>
  - Let's cut and copy all lines from code `/secret` inside `api_route.py` that we have just created;<br>
```
import time
from functools import wraps
from flask import request, jsonify
import jwt
from .token_handler import token_generator


def token_verify(function: callable) -> callable:

    # Use WRAPS to send out all contend from within internal function
    @wraps(function)
    def decorated(*args, **kwargs):

        raw_token = request.headers.get("Authorization")
        uid = request.headers.get("uid")

        if not raw_token or not uid:
            return jsonify(
                {
                    "error": "Not allowed. Must inform a user_id"
                }), 401

        try:
            if raw_token.count(" ") == 1:
                token = raw_token.split()[1]
            else:
                token = raw_token

            token_info = jwt.decode(token, key="1234", algorithms="HS256")
            token_exp = f'{(token_info["exp"] - time.time()) / 60:.2f}'
            key_uid = token_info["uid"]

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
        except KeyError:
            return jsonify(
                {
                    "error": "Invalid token. No user_id designed in token generation"
                }
            ), 401

        else:
            if not isinstance(uid, int):
                try:
                    uid = int(uid)
                except:
                    return jsonify(
                        {
                            "error": "user_id must be numbers only"
                        }
                    ), 400

            if uid != key_uid:
                return jsonify(
                    {
                        "error": "User not allowed"
                    }
                ), 401

            next_token = token_generator.refresh(token)

            print(next_token)

            return function(next_token, token_exp, *args, **kwargs)

    return decorated
```
<br>

- EXPORT this function and the singleton variable in `/scr/main/auth_jwt/__init__.py` (do not export TokenGenerator):<br>
```
<file:/scr/main/auth_jwt/__init__.py>

from .token_handler import token_generator
from .token_verifier import token_verify
```
<br>

- GO BACK in route, finish the configutation by puting the decorator just created to tell python to perfomr 
authorization check before process inside the route. (Remember that the vast majority of the old code were cut and 
copied into the decorator):
```
from flask import Blueprint, jsonify
from ..auth_jwt import token_generator, token_verify

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
```
<br>

- AJUST `/auth` route to generate a token using those new features:<br>
```
@api_routes_bp.route('/auth', methods=["POST"])
def authorization_route():

    token = token_generator.generate(uid=10)
    
    print(token)
    return jsonify(
        {
            "token": token
        }
    ), 200
```
<br>

### TEST<br>
Launch the server and run the tests:<br>
1. GENERATE A NEW TOKEN FIRST:<br>
  <img src="images/jwt-token-generator-200.png" alt="jwt-token-generator-200" width="" height=""><br>
2. TRY TO GET A 200 RESPONSE USING THE AUTHORIZATION AND THE USER_ID AS HEADERS:<br>
   <img src="images/jwt-authorization-200-2.png" alt="jwt-auhtorization-200-2" width="" height=""><br>
3. PLAY WITH ERRORS - You should get the same erros as tested before<br>
<br>

### APPLY AUTHORIZATION DECORATOR FOR ALL ROUTES<br>

Time to finish this project and get everything working. Let's mark with de `@token_verify` decorator on top of our other
routes:<br>

```
@api_routes_bp.route("/api/users", methods=["POST"])
@token_verify
def register_user(token, exp):
    """register user route"""
    ...
    
    
@api_routes_bp.route("/api/pets", methods=["POST"])
@token_verify
def register_pet(token, exp):
    """register pet route"""
    ...


@api_routes_bp.route("/api/users", methods=["GET"])
@token_verify
def find_user(token, exp):
    """find user route"""


@api_routes_bp.route("/api/pets", methods=["GET"])
@token_verify
def find_pet(token, exp):
    """find pet route"""
    ...
    
```
<br>

<strong>This way, everything should be working fine!</strong><br>
Tanks =D
