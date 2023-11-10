from ..app import app
from flask import request
from ..models.models import Group, GroupMember
from ..utils import db

def isGroupMember(group, user_id):
    pass

def isGroupAdmin(group, user_id):
    pass

@app.route("/groups", methods=["GET"])
def get_groups_api():
    # This should only return the groups relevant to the user
    return db.get_json_array(db.get_entries(Group))

@app.route("/group/<int:groupId>", methods=["GET"])
def get_group_api(groupId: int):
    # Need to check if the user making the request is in the group
    return (db.get_entry_by_id(Group, groupId)).get_dict()

@app.route("/group", methods=["POST"])
def new_group_api():
    body = request.get_json()
    new_group = Group(**body)
    return db.add_object(new_group)

@app.route("/group/<int:id>", methods=["DELETE"])
def delete_group_api(id):
    # Need to check if the user making the request is an admin of the group
    group = db.get_entry_by_id(Group ,id)
    return db.delete_object(Group)

@app.route("/group/<int:groupId>/members", methods=["GET"])
def get_group_members_api(groupId: int):
    # Need to check if the user making the request is in the group
    with db.get_session() as s:
        try:
            return db.get_json_array(s.scalars(db.select(GroupMember).where(GroupMember.group_id == groupId)).all())
        except:
            return None

@app.route("/group/<int:groupId>/member", methods=["POST"])
def new_group_member_api(groupId: int):
    body = request.get_json()
    # Need to check if the user making the request is an admin of the group
    new_group_member = GroupMember(**body)
    return db.add_object(new_group_member)

@app.route("/group/<int:groupId>/member/<int:memberId>", methods=["PATCH"])
def new_group_member_api(groupId: int, memberId: int):
    pass
    body = request.get_json()
    # Need to check if the user making the request is an admin of the group
    new_group = GroupMember(**body)
    return db.add_object(new_group)

@app.route("/group/<int:id>", methods=["DELETE"])
def delete_group_member_api(id):
    group = db.get_entry_by_id(Group ,id)
    return db.delete_object(group)
