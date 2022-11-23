from typing import Type, Dict
from src.presenters.interface import RouteInterface
from src.domain.use_cases import FindPetInterface as FindPet
from src.presenters.erros import HttpErrors
from src.presenters.helpers import HttpRequest, HttpResponse


class FindPetController(RouteInterface):
    """ Class to define controller for find pet use case """

    def __init__(self, find_pet_usecase: Type[FindPet]):
        self.find_pet_usecase = find_pet_usecase

    def route(self, http_request: Type[HttpRequest]) -> HttpResponse:
        """
        Method to call use case find pet
        :param http_request: HTTP format query request
        :return: HTTP Response
        """

        response: Dict = {}

        # check if query exists
        if http_request.query is not None:

            pet_id = http_request.query.get("pet_id")
            user_id = http_request.query.get("user_id")

            # check which keys there is in query
            if pet_id is not None and user_id is not None:
                response = self.find_pet_usecase.by_pet_id_and_user_id(pet_id=pet_id, user_id=user_id)

            elif pet_id is not None and user_id is None:
                response = self.find_pet_usecase.by_pet_id(pet_id=pet_id)

            elif user_id is not None and pet_id is None:
                response = self.find_pet_usecase.by_user_id(user_id=user_id)

            else:
                response = self.find_pet_usecase.by_pet_id_and_user_id(pet_id=None, user_id=None)

            if not response["success"]:
                http_error = HttpErrors.error_422(detail=response["detail"])
                return HttpResponse(status_code=http_error["status_code"], body=http_error["body"])

            return HttpResponse(status_code=200, body=response["data"])

        else:
            http_error = HttpErrors.error_400()
            return HttpResponse(status_code=http_error["status_code"], body=http_error["body"])
