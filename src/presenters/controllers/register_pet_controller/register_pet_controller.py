from typing import Type
from src.presenters.interface import RouteInterface
from src.domain.use_cases import RegisterPetInterface as RegisterPet
from src.presenters.erros import HttpErrors
from src.presenters.helpers import HttpRequest, HttpResponse


class RegisterPetController(RouteInterface):
    """ Class to define controller to register pet """

    def __init__(self, register_pet_usecase: [RegisterPet]):
        self.register_pet_usecase = register_pet_usecase

    def route(self, http_request: Type[HttpRequest]) -> HttpResponse:
        """
        Method to call use case register pet
        :param http_request: HttpRequest class format
        :return: HttpResponse format
        """

        response = {}

        if http_request.body:
            # if body in http_request
            body_integrity = http_request.body.keys()
            if ("petname" in body_integrity) and ("specie" in body_integrity) and ("age" in body_integrity) and \
                    ("user_id" in body_integrity):
                petname = http_request.body["petname"]
                specie = http_request.body["specie"]
                age = http_request.body["age"]
                user_id = http_request.body["user_id"]

                response = self.register_pet_usecase.register(
                    petname=petname,
                    specie=specie,
                    age=age,
                    user_id=user_id
                )
            else:
                response = {"success": False, "data": None, "detail": 'Could not procede with register pet'}

            if response["success"] is False:
                http_error = HttpErrors.error_422(detail=response["detail"])
                return HttpResponse(status_code=http_error["status_code"], body=http_error["body"])

            return HttpResponse(status_code=200, body=response["data"])

        else:
            http_error = HttpErrors.error_400()
            return HttpResponse(status_code=http_error["status_code"], body=http_error["body"])
