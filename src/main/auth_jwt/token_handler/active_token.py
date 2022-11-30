class ActiveToken:

    def __init__(self):
        self.__uid = None
        self.__token = None
        self.__username = None

    def get_token(self):
        return {"token": self.__token, "uid": self.__uid, "username": self.__username}

    def fix_token(self, new_token: str, new_uid: int, username: str):
        self.__token = new_token
        self.__uid = new_uid
        self.__username = username
