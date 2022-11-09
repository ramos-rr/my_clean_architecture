from typing import List
from src.data.interfaces import PetRepositoryInterface
from src.domain.models import Pets
from src.infra.errors import ErrorManager, NoResultFoundError
from datetime import datetime
from faker import Faker

fake = Faker()
fake_pet_id = fake.random_number(digits=5)


class PetRepositorySpy(PetRepositoryInterface):
    """
    Class to manage PET REPOSITORY SPY
    """

    def __init__(self, pet_id=fake_pet_id, user_id=fake.random_number(digits=5)):

        self.pet_id = pet_id
        self.user_id = user_id
        self.pet_name = fake.first_name()
        self.specie = 'dog'
        self.age = 0
        self.register_date = datetime.now()

    @classmethod
    def insert_pet(cls, petname: str, specie: str, age: int, user_id: int) -> Pets:
        """
        Method to mock insertion of a new pet
        :param petname: Pet name
        :param specie: Pet specie (from AnimalTypes list)
        :param age: Pet age
        :param user_id: Pet owner id
        :return: Class Pets (domain)
        """
        # VALIDATE DATA: petname, specie, age, user_id
        petname, specie, age, user_id = cls.__validate_insert_pet(petname, specie, age, user_id)

        return Pets(
            id=fake_pet_id,
            petname=petname,
            specie=specie,
            age=age,
            user_id=user_id,
            register_date=datetime.now()
        )

    def select_pet(self, pet_id=None, user_id=None) -> List[Pets]:
        """
        Method to mock the selection of one or more pets from DB
        :param pet_id: Pet ID
        :param user_id: Pet owner ID
        :return: List of PETS
        """
        # VALIDATE SELECT PETS REQUIRED DATA:
        pet_id, user_id = self.__validate_select_pet(pet_id, user_id)

        if pet_id and not user_id:
            try:
                if pet_id == self.pet_id:
                    return self.__return_pet()
                else:
                    raise Exception
            except Exception:
                raise NoResultFoundError(message='No row was found when one was required', code=None)

        elif user_id and not pet_id:
            try:
                if user_id == self.user_id:
                    return self.__return_pet()
                else:
                    raise Exception
            except Exception:
                raise NoResultFoundError(message='No row was found when one was required', code=None)

        elif pet_id and user_id:
            try:
                if user_id == self.user_id:
                    return self.__return_pet()
                else:
                    raise Exception
            except Exception:
                raise NoResultFoundError(message='No row was found when one was required', code=None)

    @classmethod
    def __validate_insert_pet(cls, petname, specie, age, user_id):
        ErrorManager.validate_insert_pet(petname, specie, age, user_id)
        return petname, specie, age, user_id

    @classmethod
    def __validate_select_pet(cls, pet_id, user_id):
        ErrorManager.validate_select_pet(pet_id=pet_id, user_id=user_id)
        return pet_id, user_id

    def __return_pet(self):
        return [Pets(
            id=self.pet_id,
            petname=self.pet_name,
            specie=self.specie,
            age=self.age,
            user_id=self.user_id,
            register_date=self.register_date
        )]
