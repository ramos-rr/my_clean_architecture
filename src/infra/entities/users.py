from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from src.infra.config import Base
from sqlalchemy.sql.functions import now


class Users(Base):
    """ Users Entity"""

    # Set Table username
    __tablename__ = "users"
    # Set ID as COLUMN, and primary_key=True (means this is a primary key)
    id = Column(Integer, primary_key=True)
    # Set NAME as Column, string, not Null and Unique=True
    username = Column(String, nullable=False, unique=True)
    # Set PASSWORD as Column, string and not Null
    password = Column(String, nullable=False)
    # Set PET_ID as a relationship with pets class
    pet_id = relationship("Pets")
    # Register date
    register_date = Column(DateTime(timezone=True), onupdate=now())

    # Set a string for verification (DB pattern)
    def __rep__(self):
        return f'Urs [username={self.username}]'

    # Compare this class to an outer class to check the similarities
    def __eq__(self, other):
        if (self.id == other.id) and (self.username == other.username) and (self.password == other.password):
            return True
        return False
