from typing import List, Type
from src.infra.config import DbConnectionHandler
from src.infra.entities.pets import Pets as PetsEntity
from src.domain.models import Pets
from src.infra.errors import ErrorManager
from datetime import datetime


class PetRepository:
    """
    Class to manage PET REPOSITORY
    """
    @classmethod
    def insert_pet(cls, petname: str, specie: str, age: int, user_id: int) -> Pets:
        """
        Method to insert new pet
        :param petname: Pet name
        :param specie: Pet specie (from AnimalTypes list)
        :param age: Pet age
        :param user_id: Pet owner id
        :return: Class Pets (domain)
        """
        # VALIDATE DATA: petname, specie, age, user_id
        petname, specie, age, user_id = cls.__validate_insert_pet(petname, specie, age, user_id)

        try:
            with DbConnectionHandler() as db_conn:
                new_pet = PetsEntity(petname=petname, specie=specie, age=age, user_id=user_id,
                                     register_date=datetime.now())
                db_conn.session.add(new_pet)
                db_conn.session.commit()
                return Pets(
                    id=new_pet.id,
                    petname=new_pet.petname,
                    specie=new_pet.specie.value,
                    age=new_pet.age,
                    user_id=new_pet.user_id,
                    register_date=new_pet.register_date
                )
        except Exception as error:
            try:
                error.__getattribute__('code')
            except:
                ErrorManager.database_error(error.args)
            else:
                ErrorManager.database_error(error.args, error.code)
            db_conn.session.rollback()
        finally:
            db_conn.session.close()

    @classmethod
    def select_pet(cls, pet_id=None, user_id=None) -> List[Pets]:
        """
        Method to select one or more pets from DB
        :param pet_id: Pet ID
        :param user_id: Pet owner ID
        :return: List of PETS
        """
        # VALIDATE SELECT PETS REQUIRED DATA:
        pet_id, user_id = cls.__validate_select_pet(pet_id, user_id)

        try:
            with DbConnectionHandler() as db_conn:
                if pet_id and not user_id:
                    data = db_conn.session.query(PetsEntity).filter_by(id=pet_id).one()
                    data = cls.__get_specie_string(data)
                    query_data = data
                elif user_id and not pet_id:
                    data = db_conn.session.query(PetsEntity).filter_by(user_id=user_id).all()  # ALL() -> return every
                    # pet owned by the same user_id
                    data = cls.__get_specie_string(data)
                    query_data = data
                elif pet_id and user_id:
                    data = db_conn.session.query(PetsEntity).filter_by(id=pet_id, user_id=user_id).one()
                    data = cls.__get_specie_string(data)
                    query_data = data
            return query_data

        except Exception as error:
            try:
                error.__getattribute__('code')
            except:
                ErrorManager.database_error(error.args)
            else:
                ErrorManager.database_error(error.args, error.code)
            db_conn.session.rollback()

        finally:
            db_conn.session.close()

    @classmethod
    def __get_specie_string(cls, data: List | Type[PetsEntity]):
        if isinstance(data, List):
            for pet in data:
                pet.specie = pet.specie.value
            return data
        elif isinstance(data, PetsEntity):
            data.specie = data.specie.value
            return [data]

    @classmethod
    def __validate_insert_pet(cls, petname, specie, age, user_id):
        ErrorManager.validate_insert_pet(petname, specie, age, user_id)
        return petname, specie, age, user_id

    @classmethod
    def __validate_select_pet(cls, pet_id, user_id):
        ErrorManager.validate_select_pet(pet_id=pet_id, user_id=user_id)
        return pet_id, user_id
