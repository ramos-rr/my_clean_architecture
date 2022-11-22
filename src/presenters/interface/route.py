from abc import ABC, abstractmethod
from typing import Type
from src.presenters.helpers import HttpRequest, HttpResponse


class RouteInterface(ABC):
    """ Interface class to Route """

    @abstractmethod
    def route(self, http_request: Type[HttpRequest]) -> HttpResponse:
        """ Method to define route """
        raise NotImplementedError("You must implement this method")
