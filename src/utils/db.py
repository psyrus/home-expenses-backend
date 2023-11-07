from sqlalchemy.orm import Session
from sqlalchemy import engine
from sqlalchemy import select
import json
import logging
from ..databases.database_interface import DatabaseSingleton
from ..models.models import Base, User, AccessToken
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime
load_dotenv(dotenv_path=os.path.join(os.getcwd(), "src", ".env"))


_engine = DatabaseSingleton()

def get_engine() -> engine:
    return _engine

def get_session() -> Session:
    engine = get_engine()
    return Session(engine)

def add_object(obj: Base) -> dict | str:
    with get_session() as s:
        try:
            s.add(obj)
            s.commit()
            logging.debug("Object added successfully: %s" % obj.get_dict())
            return obj.get_dict()
        except Exception as e:
            s.rollback()
            logging.error(e)
            return e.orig.args[0]

def is_jwt_valid(jwt_token: str, secret_key: str) -> bool:
    if not jwt_token:
        return False

    is_valid = False
    try:
        decoded_jwt=jwt.decode(jwt_token, secret_key, algorithms=["HS256"], verify=True)
    except:
        return False

    with get_session() as s:
        try:
            user_ref = s.scalars(select(User).where(User.auth_provider_id == decoded_jwt['sub'])).one()
            jwt_ref = s.scalars(select(AccessToken).where(AccessToken.registered_to_user == user_ref.id).where(AccessToken.token_value == jwt_token)).one()
            if jwt_ref.expires >= datetime.now():
                is_valid = True
            else:
                delete_object(jwt_ref, s)
        except Exception as e:
            pass
    return is_valid

def get_entry_by_id(class_type: Base, id: int) -> Base:
    db_select = select(class_type).where(class_type.id == id)
    
    with get_session() as s:
        try:
            db_entry = s.scalars(db_select).one()
            logging.debug(db_entry)
            logging.debug(db_entry.get_dict())
        except:
            return None
            
        return db_entry

def get_entries(class_type: Base) -> list[Base]:
    db_select = select(class_type)
    
    with get_session() as s:
        db_entries = s.scalars(db_select).all()
        logging.debug(get_json_array(db_entries))
            
        return db_entries

def get_json_single(db_object: Base) -> dict:
    return db_object.get_dict()

def get_json_array(db_object_list: list[Base]) -> dict:
    output = [i.get_dict() for i in db_object_list]
    return output

def delete_object(obj: Base, session: Session = None) -> dict | str:
    if obj == None:
        return "Entity in database did not exist"
    with session or get_session() as s:
        try:
            s.delete(obj)
            s.commit()
            return "Object deleted successfully: %s" % obj.get_dict()
        except Exception as e:
            s.rollback()
            logging.error(e)
            return e.orig.args[0]
        
def update_object_properties(obj: Base, patch: dict) -> None:
    obj_dict = obj.get_dict()
    for key in obj_dict.keys():
        if key not in patch:
            continue
        setattr(obj, key, patch[key])
    logging.debug(obj_dict)
    logging.debug(obj.get_dict())
