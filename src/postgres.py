
from sqlalchemy import (Column, Integer, String, Unicode, UnicodeText,
                        create_engine)
from sqlalchemy.orm import Session

from models import user, test
from models.base import Base

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/postgres")

Base.metadata.create_all(engine)

with Session(engine) as s:
    # create instances of my user object
    u = user.User('nosklo')
    u.address = '66 Some Street #500'

    u2 = user.User('lakshmipathi')
    u2.password = 'ihtapimhskal'

    # testing
    s.add_all([u, u2])
    s.commit()
    
    t1 = test.Test("test1")
    t2 = test.Test("test2")
    
    s.add_all([t1, t2])
    
    s.commit()