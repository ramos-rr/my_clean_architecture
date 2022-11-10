from typing import Type, Dict
from src.presenters.helpers import HttpRequest, HttpResponse
from src.domain.use_cases.find_user import FindUserInterface as FindUser
from src.presenters.erros import HttpErrors


class FindUserController:
    """ Class to define controller to find_user usecase """

    def __init__(self, find_user_use_case: Type[FindUser]):
        self.find_user_use_case = find_user_use_case

    def handle(self, http_request: Type[HttpRequest]) -> HttpResponse:
        """
        Method to call use case to find_user
        :param http_request: Protocol to perform HTTP Request
        :return: HTTP response protocol
        """
        response: Dict = {}

        if http_request.query:
            # check if query
            query_string_params = http_request.query.keys()

            if "user_id" in query_string_params and "username" in query_string_params:
                user_id = http_request.query["user_id"]
                username = http_request.query["username"]
                response = self.find_user_use_case.by_user_id_and_username(user_id=user_id, username=username)

            elif "user_id" in query_string_params and "username" not in query_string_params:
                user_id = http_request.query["user_id"]
                response = self.find_user_use_case.by_user_id(user_id=user_id)

            elif "user_id" not in query_string_params and "username" in query_string_params:
                username = http_request.query["username"]
                response = self.find_user_use_case.by_username(username=username)

            else:
                response = {"success": False, "data": None}

            if response["success"] is False:
                http_error = HttpErrors.error_422(detail=response['detail'])
                return HttpResponse(
                    status_code=http_error["status_code"],
                    body=http_error["body"],
                )

            return HttpResponse(status_code=200, body=response["data"])

        else:
            http_error = HttpErrors.error_400()
            return HttpResponse(
                status_code=http_error["status_code"],
                body=http_error["body"]
            )
