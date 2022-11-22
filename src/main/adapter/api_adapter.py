from typing import Type
from src.presenters.interface import RouteInterface as Route
from src.presenters.helpers import HttpRequest


def flask_adapter(request: any, api_route: Type[Route]) -> any:
    """
    Adapter patterns to flask
    :param request: Flask Request
    :param api_route: Composite route
    return: Any
    """

    http_request = HttpRequest(body=request.json)
    response = api_route.route(http_request=http_request)

    return response
