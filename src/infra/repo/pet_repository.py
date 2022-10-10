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
        """
        # VALIDATE DATA: petname, specie, age, user_id
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
            ErrorManager.database_error(error.args, error.code)
            db_conn.session.rollback()
        finally:
            db_conn.session.close()
