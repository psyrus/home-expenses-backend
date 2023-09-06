from ..app import app
from ..utils import *
from flask import request
from ..models.models import User,Group
from ..models.base import Base
import json

def get_user_helper(id:int) -> User:
    with get_session() as s:
        try:
            return s.scalars(select(User).where(User.id == id)).one()
        except:
            return None

def get_user_helper_authid(oid):
    with get_session() as s:
        try:
            return s.scalars(select(User).where(User.auth_provider_id == oid)).one()
        except:
            return None

# User
@app.route("/users", methods=["GET"])
def get_users_api():
    return get_json_array(get_db_entries(User))
    

@app.route("/user/<int:id>", methods=["GET"])
def get_user_api(id):
    user = get_user_helper(id)
    return json.loads(json.dumps(user.get_dict(), default = str))


@app.route("/user", methods=["POST"])
def new_user_api():
    username = request.get_json()['username']
    return add_object_to_database(User(username=username))


@app.route("/user/<int:id>", methods=["DELETE"])
def delete_user_api(id):
    user = get_user_helper(id)
    return delete_object_from_database(user)


@app.route("/user/<int:id>", methods=["PATCH"])
def update_user_api(id):
    req = request.get_json()
    s = get_session()
    s.begin()
    user = s.scalars(select(User).where(User.id == id)).one()
    update_object_properties(user, req)
    s.commit()
    s.close()
    return "update user %s" % id


@app.route("/user/<int:id>/groups", methods=["GET"])
def get_user_groups_api(id):
    with get_session() as s:
        try:
            groups = s.scalars(select(Group).where(Group.created_by == id)).all()
        except:
            return None
    return get_json_array(groups)