from typing import Type
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

        response = {}

        # check if query exists
        if http_request.query is not None:

            http_query_keys = http_request.query.keys()

            # check which keys there is in query
            if ("pet_id" in http_query_keys) and ("user_id" not in http_query_keys):
                pet_id = http_request.query["pet_id"]
                response = self.find_pet_usecase.by_pet_id(pet_id=pet_id)

            elif ("pet_id" not in http_query_keys) and ("user_id" in http_query_keys):
                user_id = http_request.query["user_id"]
                response = self.find_pet_usecase.by_user_id(user_id=user_id)

            elif ("pet_id" in http_query_keys) and ("user_id" in http_query_keys):
                pet_id = http_request.query["pet_id"]
                user_id = http_request.query["user_id"]
                response = self.find_pet_usecase.by_pet_id_and_user_id(pet_id=pet_id, user_id=user_id)

            if not response["success"]:
                http_error = HttpErrors.error_422(detail=response["detail"])
                return HttpResponse(status_code=http_error["status_code"], body=http_error["body"])

            return HttpResponse(status_code=200, body=response["data"])

        else:
            http_error = HttpErrors.error_400()
            return HttpResponse(status_code=http_error["status_code"], body=http_error["body"])
