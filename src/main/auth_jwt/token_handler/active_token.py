class ActiveToken:

    def __init__(self):
        self.__uid = None
        self.__token = None

    def get_token(self):
        return self.__token, self.__uid

    def fix_token(self, new_token: str, new_uid: int):
        self.__token = new_token
        self.__uid = new_uid
