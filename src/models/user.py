from .base import Base
from random import choice

from sqlalchemy import (Column, Integer, String, Unicode, UnicodeText, DateTime,
                        create_engine)
from sqlalchemy.orm import DeclarativeBase, Session
import string

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(40))
    address = Column(UnicodeText, nullable=True)
    password = Column(String(20))

    def __init__(self, name, address=None, password=None):
        self.name = name
        self.address = address
        if password is None:
            password = ''.join(choice(string.ascii_letters) for n in range(10))
        self.password = password