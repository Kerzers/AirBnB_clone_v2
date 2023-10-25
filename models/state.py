#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        """
        Getter attribute to retrieve a list of City instances with
        state_id equals to the current State.id for FileStorage.
        """
        cities = []
        instances = storage.all(City)
        for obj in instances.values():
            if (obj.__class__ == 'City'):
                cities.append(obj)
        return [city for city in cities if city.state_id == self.id]
