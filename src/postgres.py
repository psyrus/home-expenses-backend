
from sqlalchemy import (Column, Integer, String, Unicode, UnicodeText,
                        create_engine)
from sqlalchemy.orm import Session

from models.models import *
from models.base import Base
import random
import string
from sqlalchemy import select

engine = create_engine(
    "postgresql+psycopg://postgres:postgres@localhost:5432/backend")

Base.metadata.create_all(engine)

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

usernames = [get_random_string(5) for i in range(5)]

with Session(engine) as s:
    # create instances of my user object
    new_users = [User(username=u) for u in usernames]

    # testing
    try:
        s.add_all(new_users)
        s.commit()
    except:
        s.rollback()

    users = select(User)

    for user in s.scalars(users):
        print(user)
