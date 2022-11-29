from typing import Type
from src.infra.errors import InsufficientDataError
from src.presenters.interface import RouteInterface
from src.presenters.helpers import HttpRequest, HttpResponse
from src.domain.use_cases.find_user import FindUserInterface as FindUser
from src.presenters.erros import HttpErrors


class FindUserController(RouteInterface):
    """ Class to define controller to find_user usecase """

    def __init__(self, find_user_use_case: [FindUser]):
        self.find_user_use_case = find_user_use_case

    def route(self, http_request: Type[HttpRequest]) -> HttpResponse:
        """
        Method to call use case to find_user
        :param http_request: Protocol to perform HTTP Request
        :return: HTTP response protocol
        """
        response = dict()

        # check if query
        if http_request.query is not None:

            username = http_request.query.get("username")
            user_id = http_request.query.get("user_id")

            if username is not None and user_id is not None:
                response = self.find_user_use_case.by_user_id_and_username(user_id=user_id, username=username)

            elif user_id is not None and username is None:
                response = self.find_user_use_case.by_user_id(user_id=user_id)

            elif username is not None and user_id is None:
                response = self.find_user_use_case.by_username(username=username)

            else:
                response = self.find_user_use_case.by_username(username=username)

            if response["success"] is False:
                http_error = HttpErrors.error_422(detail=response['detail'])
                return HttpResponse(
                    status_code=http_error["status_code"],
                    body=http_error["body"],
                )

            return HttpResponse(status_code=200, body=response["data"])

        else:
            http_error = HttpErrors.error_400(detail=InsufficientDataError('No query has been requested! Please '
                                                                           'check if parameters are correctly written'))
            return HttpResponse(
                status_code=http_error["status_code"],
                body=http_error["body"]
            )
