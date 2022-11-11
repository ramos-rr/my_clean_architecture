from typing import Type
from src.presenters.erros import HttpErrors
from src.domain.use_cases import RegisterUserInterface as RegisterUser
from src.presenters.helpers import HttpRequest, HttpResponse


class RegisterUserController:
    """ Class to define controller for register user use case """

    def __init__(self, register_user_usecase: Type[RegisterUser]):
        self.register_user_usecase = register_user_usecase

    def handle(self, http_request: Type[HttpRequest]) -> HttpResponse:
        """
        Method to call register user use case
        :param http_request: HTTP request body
        :return: HTTP Response
        """

        response = {}

        # check if body is present
        if http_request.body:

            http_body_keys = http_request.body.keys()

            if ("username" in http_body_keys) and ("password" in http_body_keys):
                username = http_request.body["username"]
                password = http_request.body["password"]

                response = self.register_user_usecase.register(name=username, password=password)

            if not response["success"]:
                http_error = HttpErrors.error_422(detail=response["detail"])
                return HttpResponse(status_code=http_error["status_code"], body=http_error["body"])

            return HttpResponse(status_code=200, body=response["data"])

        else:
            http_error = HttpErrors.error_400()
            return HttpResponse(status_code=http_error["status_code"], body=http_error["body"])
