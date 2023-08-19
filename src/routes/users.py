from ..app import app
from ..utils import *
from flask import request
from ..models.models import User
from ..models.base import Base
import json

def get_user_helper(id):
    with get_session() as s:
        return s.scalars(select(User).where(User.id == id)).one()

# User
@app.route("/users", methods=["GET"])
def get_users():
    return get_json_array(get_db_entries(User))
    

@app.route("/user/<int:id>", methods=["GET"])
def get_user(id):
    user = get_user_helper(id)
    return json.loads(json.dumps(user.get_dict(), default = str))


@app.route("/user", methods=["POST"])
def new_user():
    username = request.get_json()['username']
    return add_object_to_database(User(username=username))


@app.route("/user/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = get_user_helper(id)
    return delete_object_from_database(user)


@app.route("/user/<int:id>", methods=["PATCH"])
def update_user(id):
    req = request.get_json()
    s = get_session()
    s.begin()
    user = s.scalars(select(User).where(User.id == id)).one()
    # user = update_object_properties(user, req)
    user.username = req['username']
    s.commit()
    s.close()
    return "update user %s" % id
