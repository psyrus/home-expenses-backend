
from sqlalchemy import (Column, Integer, String, Unicode, UnicodeText,
                        create_engine)
from sqlalchemy.orm import Session

from models.models import *
from models.base import Base

from sqlalchemy import select

engine = create_engine(
    "postgresql+psycopg://postgres:postgres@localhost:5432/backend")

Base.metadata.create_all(engine)


with Session(engine) as s:
    # create instances of my user object
    u = User(username='TRevor')
    u2 = User(username='kyoka')

    # testing
    try:
        s.add_all([u, u2])
        s.commit()
    except:
        s.rollback()

    users = select(User)

    for user in s.scalars(users):
        print(user)
