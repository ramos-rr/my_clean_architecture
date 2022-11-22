from typing import Type
from src.presenters.interface import RouteInterface
from src.presenters.erros import HttpErrors
from src.domain.use_cases import RegisterUserInterface as RegisterUser
from src.presenters.helpers import HttpRequest, HttpResponse


class RegisterUserController(RouteInterface):
    """ Class to define controller for register user use case """

    def __init__(self, register_user_usecase: Type[RegisterUser]):
        self.register_user_usecase = register_user_usecase

    def route(self, http_request: Type[HttpRequest]) -> HttpResponse:
        """
        Method to call register user use case
        :param http_request: HTTP request body
        :return: HTTP Response
        """

        response = {}

        # check if body is present
        if http_request.body:

            username = http_request.body.get("username")
            password = http_request.body.get("password")

            response = self.register_user_usecase.register(name=username, password=password)

            if (response.get("success") is None) or (not response.get("success")):
                http_error = HttpErrors.error_422(detail=response["detail"])
                return HttpResponse(status_code=http_error["status_code"], body=http_error["body"])

            return HttpResponse(status_code=200, body=response["data"])

        else:
            http_error = HttpErrors.error_400()
            return HttpResponse(status_code=http_error["status_code"], body=http_error["body"])
