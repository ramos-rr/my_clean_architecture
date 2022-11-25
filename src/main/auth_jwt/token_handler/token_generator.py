from datetime import datetime, timedelta
import time
import jwt


class TokenGenerator:
    """ Class to create and refresh tokens """
    def __init__(self, token_key: str, exp_time_min: int, refresh_time_min):
        self.__TOKEN_KEY = token_key
        self.__EXP_TIME_MIN = exp_time_min
        self.__REFRESH_TIME_MIN = refresh_time_min

    def generate(self, uid: int) -> str:
        """
        Method to generate a new token
        :param uid: User ID to be linked to this new token
        :return: New Token string
        """
        return self.__encode_token(uid=uid)

    def refresh(self, token: str) -> str:
        """
        Method to check and refresh token expiration time when needed. It takes in account how many minutes were defined
        in class instatiation
        :param token: Token already bein used
        :return: New Token string or the same Token string
        """
        token_info = jwt.decode(token, key=self.__TOKEN_KEY, algorithms="HS256")
        uid = token_info["uid"]
        exp = token_info["exp"]

        if ((exp - time.time()) / 60) < self.__REFRESH_TIME_MIN:
            return self.__encode_token(uid=uid)

        return token

    def __encode_token(self, uid: int) -> str:
        """
        Private method to generate a new token
        :param uid: User ID to be linked to this new token
        :return: New Token string
        """
        token = jwt.encode(
            {
                "exp": datetime.utcnow() + timedelta(minutes=self.__EXP_TIME_MIN),
                "uid": uid
            },
            key=self.__TOKEN_KEY,
            algorithm="HS256"
        )
        return token
