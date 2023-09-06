from ..app import app
from ..utils import *
from flask import request, abort
from ..models.models import Group
from ..models.base import Base
from .users import get_user_helper

# Group
@app.route("/groups", methods=["GET"])
def get_groups_api():
    groups = get_db_entries(Group)
    return get_json_array(groups)

@app.route("/group/<int:id>", methods=["GET"])
def get_group_api(id):
    group = get_db_entry_by_id(Group, id)
    if not group:
        abort(404)
        
    return group.get_dict()
    # with get_session() as s:
    #     try:
    #         return s.scalars(select(Group).where(Group.id == id)).one()
    #     except:
    #         abort(404)  # 404 Not Found
    #         abort(Response('Hello World'))


@app.route("/group", methods=["POST"])
def new_group_api():
    request_data = request.get_json()
    group_name = request_data['group_name']
    
    created_by_user = get_user_helper(request_data['created_by'])
    if not created_by_user:
        abort(401)
    
    return add_object_to_database(Group(group_name=group_name, created_by=created_by_user.id)).get_dict()


@app.route("/group/<int:id>", methods=["DELETE"])
def delete_group_api(id):
    group = get_db_entry_by_id(Group, id)
    return delete_object_from_database(group)


@app.route("/group/<int:id>", methods=["PATCH"])
def update_group_api(id):
    req = request.get_json()
    s = get_session()
    s.begin()
    group = s.scalars(select(Group).where(Group.id == id)).one()
    # group = get_db_entry_by_id(Group, id)
    update_object_properties(group, req)
    s.commit()
    s.close()
    return group.get_dict()
