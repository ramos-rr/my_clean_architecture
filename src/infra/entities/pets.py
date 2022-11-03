import enum
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum as SqlEnum
from src.infra.config.db_base import Base
import datetime


class AnimalTypes(enum.Enum):
    """ Defining species for Pets to build up a list of allowed species"""

    dog = 'dog'
    cat = 'cat'
    fish = 'fish'
    bird = 'bird'
    reptile = 'reptile'


class Pets(Base):
    """ Pets Entity """

    # Set up TABLE NAME
    __tablename__ = 'pets'
    # Set up ID, primary_key=True
    id = Column(Integer, primary_key=True)
    # Set up NAME
    petname = Column(String(20), nullable=False, unique=True)
    specie = Column(SqlEnum(AnimalTypes), nullable=False)
    age = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    register_date = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now())

    def __rep__(self):
        return f'Pet: [name={self.petname}, specie={self.specie}, user_id={self.user_id}]'

    def __eq__(self, other):
        if (self.id == other.id) and \
                (self.petname == other.petname) and \
                (self.specie == other.specie) and \
                (self.user_id == other.user_id) and\
                (self.age == other.age):
            return True
        return False
