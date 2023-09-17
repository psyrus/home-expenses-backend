from sqlalchemy.orm import Session
from sqlalchemy import (create_engine, engine)
import sqlalchemy
from sqlalchemy import select
import json
from .models.models import Base
from sqlalchemy import (create_engine)
from sqlalchemy_utils import database_exists, create_database, drop_database
from .models.base import Base

def get_engine(engine_endpoint: str = "postgresql+psycopg://postgres:postgres@localhost:5432/backend") -> sqlalchemy.Engine:
    return create_engine(engine_endpoint)

def get_session(engine_endpoint: str = "", engine: sqlalchemy.Engine = None) -> Session:
    if not engine:
        engine = get_engine(engine_endpoint)
    return Session(engine)

def reset_db(engine: sqlalchemy.Engine) -> None:
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)
    Base.metadata.create_all(engine)

def get_test_engine_endpoint(suffix: int) -> str:
    return "postgresql+psycopg://postgres:postgres@localhost:5432/backend%s" % suffix

def remove_test_database(engine_url: str) -> None:
    drop_database(engine_url)

def add_object_to_database(obj: Base) -> dict | str:
    with get_session() as s:
        try:
            s.add(obj)
            s.commit()
            print("Object added successfully: %s" % repr(obj))
            return obj.get_dict()
        except Exception as e:
            s.rollback()
            print(e)
            return e.orig.args[0]

def get_db_entry_by_id(class_type: Base, id: int) -> Base:
    db_select = select(class_type).where(class_type.id == id)
    
    with get_session() as s:
        try:
            db_entry = s.scalars(db_select).one()
            print(db_entry)
            print(db_entry.get_dict())
        except:
            return None
            
        return db_entry

def get_db_entries(class_type: Base) -> list[Base]:
    db_select = select(class_type)
    
    with get_session() as s:
        db_entries = s.scalars(db_select).all()
        print(get_json_array(db_entries))
            
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
            print(e)
            return e.orig.args[0]
        
def update_object_properties(obj: Base, patch: dict) -> Base:
    obj_dict = obj.get_dict()
    for key in obj_dict.keys():
        if key not in patch:
            continue
        setattr(obj, key, patch[key])
    return obj
