#!/usr/bin/python3
""" dbStorage Module for HBNB project """
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """class DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the class"""
        db_user = getenv("HBNB_MYSQL_USER")
        db_pwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        db_host = getenv("HBNB_MYSQL_HOST")
        environment = getenv("HBNB_ENV")
        connection_url = f"mysql+mysqldb://{db_user}:{db_pwd}@{db_host}/{db}"

        self.__engine = create_engine(connection_url, pool_pre_ping=True)

        if environment == 'test':
            metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """ method to list all instance as a dictionary"""
        _dict = {}
        if (cls):
            if type(cls) is str:
                cls = eval(cls)
            instances = self.__session.query(cls).all()
            for obj in instances:
                if '_sa_instance_state' in obj.__dict__.keys():
                    del obj.__dict__['_sa_instance_state']
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                _dict[key] = obj
        else:
            class_list = [State, City, User, Place, Review, Amenity]
            for elmt in class_list:
                instances = self.__session.query(elmt).all()
                for obj in instances:
                    if '_sa_instance_state' in obj.__dict__.keys():
                        del obj.__dict__['_sa_instance_state']
                    key = '{}.{}'.format(elmt, obj.id)
                    _dict[key] = obj
        self.__session.close()
        return (_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """close a sesssion"""
        self.__session.remove()
