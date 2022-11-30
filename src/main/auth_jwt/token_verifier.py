import time
from decouple import config
from functools import wraps
from flask import jsonify  # , request
import jwt
from .token_handler import token_generator, active_token


def token_verify(function: callable) -> callable:

    # Use WRAPS to send out all contend from within internal function
    @wraps(function)
    def decorated(*args, **kwargs):

        active = active_token.get_token()
        raw_token = active["token"]
        uid = active["uid"]
        username = active["username"]
        # raw_token = request.headers.get("Authorization")
        # uid = request.headers.get("uid")

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

            token_info = jwt.decode(token, key=config("TOKEN_KEY"), algorithms=config("TOKEN_ALGORITHMS"))
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
            if next_token != token:
                active_token.fix_token(new_token=next_token, new_uid=uid, username=username)
                token_info = jwt.decode(token, key=config("TOKEN_KEY"), algorithms=config("TOKEN_ALGORITHMS"))
                token_exp = f'{(token_info["exp"] - time.time()) / 60:.2f}'

            print(next_token)

            return function(next_token, token_exp, username, *args, **kwargs)

    return decorated
