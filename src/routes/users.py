import jwt

from flask import request
from sqlalchemy import select

from ..app import app
from ..models.models import User
from ..utils import db


def get_user_helper(id:int) -> User:
    with db.get_session() as s:
        try:
            return s.scalars(select(User).where(User.id == id)).one()
        except:
            return None

def get_user_helper_authid(oid: str) -> User | None:
    with db.get_session() as s:
        try:
            return s.scalars(select(User).where(User.auth_provider_id == oid)).one()
        except:
            return None

def get_user_current() -> User:
    encoded_jwt=request.headers.get("Authorization").split("Bearer ")[1]
    decoded_jwt=jwt.decode(encoded_jwt, app.secret_key, algorithms=["HS256"], verify=True)
    user = get_user_helper_authid(decoded_jwt['sub'])
    return user

@app.route("/users", methods=["GET"])
def get_users_api():
    return db.get_json_array(db.get_entries(User))

@app.route("/user/<int:id>", methods=["GET"])
def get_user_api(id):
    user = get_user_helper(id)
    return user.get_dict()

@app.route("/user/me", methods=["GET"])
def get_user_current_api():
    return (get_user_current()).get_dict()

@app.route("/user", methods=["POST"])
def new_user_api():
    body = request.get_json()
    new_user = User(**body)
    return db.add_object(new_user)

@app.route("/user/<int:id>", methods=["DELETE"])
def delete_user_api(id):
    user = get_user_helper(id)
    return db.delete_object(user)


@app.route("/user/<int:id>", methods=["PATCH"])
def update_user_api(id):
    req = request.get_json()
    s = db.get_session()
    s.begin()
    user = s.scalars(select(User).where(User.id == id)).one()
    db.update_object_properties(user, req)
    s.commit()
    s.close()
    return "update user %s" % id
