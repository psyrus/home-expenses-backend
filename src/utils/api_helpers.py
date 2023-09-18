from sqlalchemy.orm import Session
from sqlalchemy import (create_engine, engine)
from sqlalchemy import select
import json
import logging
from ..models.models import Base

# log = logging.getLogger(__name__)

def get_engine() -> engine:
    return create_engine(
        "postgresql+psycopg://postgres:postgres@localhost:5432/backend")

def get_session() -> Session:
    engine = get_engine()
    return Session(engine)

def add_object_to_database(obj: Base) -> dict | str:
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

def get_db_entry_by_id(class_type: Base, id: int) -> Base:
    db_select = select(class_type).where(class_type.id == id)
    
    with get_session() as s:
        try:
            db_entry = s.scalars(db_select).one()
            logging.debug(db_entry)
            logging.debug(db_entry.get_dict())
        except:
            return None
            
        return db_entry

def get_db_entries(class_type: Base) -> list[Base]:
    db_select = select(class_type)
    
    with get_session() as s:
        db_entries = s.scalars(db_select).all()
        logging.debug(get_json_array(db_entries))
            
        return db_entries
    
def get_json_array(db_object_list: list[Base]) -> dict:
    output = [i.get_dict() for i in db_object_list]
    return json.loads(json.dumps(output, default = str))

def delete_object_from_database(obj: Base) -> dict | str:
    if obj == None:
        return "Entity in database did not exist"
    with get_session() as s:
        try:
            s.delete(obj)
            s.commit()
            return "Object deleted successfully: %s" % json.dumps(obj.get_dict())
        except Exception as e:
            s.rollback()
            logging.error(e)
            return e.orig.args[0]
        
def update_object_properties(obj: Base, patch: dict):
    obj_dict = obj.get_dict()
    for key in obj_dict.keys():
        if key not in patch:
            continue
        setattr(obj, key, patch[key])
    logging.debug(obj_dict)
    logging.debug(obj.get_dict())
