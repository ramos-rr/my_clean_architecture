from typing import Dict
from abc import ABC, abstractmethod
from src.domain.models import Users


class RegisterUserInterface(ABC):
    """ Interface to RegisterUser use case"""

    @abstractmethod
    def register(self, name, password) -> Dict[bool, Users]:
        """ register user interface """
        raise NotImplementedError("You must implement this method")
