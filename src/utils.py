from sqlalchemy.orm import Session
from sqlalchemy import (create_engine, engine)
from sqlalchemy import select, delete
import json
from .models.models import Base

def get_engine() -> engine:
    return create_engine(
        "postgresql+psycopg://postgres:postgres@localhost:5432/backend")

def get_session() -> Session:
    engine = get_engine()
    return Session(engine)

def add_object_to_database(obj: Base) -> Base:
    with get_session() as s:
        try:
            s.add(obj)
            s.commit()
            print("Object added successfully: %s" % repr(obj))
            return obj
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
    
def get_json_array(db_object_list):
    output = [i.get_dict() for i in db_object_list]
    return json.loads(json.dumps(output, default = str))

def delete_object_from_database(obj):
    with get_session() as s:
        try:
            s.delete(obj)
            s.commit()
            return "Object deleted successfully: %s" % repr(obj)
        except Exception as e:
            s.rollback()
            print(e)
            return e.orig.args[0]
        
def update_object_properties(obj, patch):
    obj_dict = obj.get_dict()
    for key in obj_dict.keys():
        if key not in patch:
            continue
        setattr(obj, key, patch[key])
    print(obj_dict)
    print(obj)
    # return obj