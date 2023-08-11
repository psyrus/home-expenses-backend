from sqlalchemy import (create_engine, select)
from sqlalchemy.orm import Session
from flask import request
import json
from ..models.models import User

from ..app import app

# Test

# def get_dict(db_object):
#     dict_ = {}
#     for key in db_object.__mapper__.c.keys():
#         dict_[key] = getattr(db_object, key)
#     return dict_

def get_session() -> Session:
    engine = create_engine(
        "postgresql+psycopg://postgres:postgres@localhost:5432/backend")
    return Session(engine)

@app.route("/test", methods=["GET"])
def get_test():
    
    engine = create_engine(
        "postgresql+psycopg://postgres:postgres@localhost:5432/backend")
    with Session(engine) as s:
        db_users = s.scalars(select(User)).all()
        users = [repr(i) for i in db_users]
        
    print(db_users[0].get_dict())
    
    print("hello")
        
    return users

@app.route("/test", methods=["POST"])
def post_test():
    username = request.get_json()['username']
    with get_session() as s:
        try:
            new_user = User(username=username)
            s.add(new_user)
            s.commit()
        except Exception as e:
            s.rollback()
            print(e)
            return "failed"

    return "Success"