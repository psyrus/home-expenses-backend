from flask import abort, request

from ..app import app
from ..models.models import Group, GroupMember
from ..utils import db
from ..utils.authorization import public_endpoint
from .users import get_user_current

import logging
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def isGroupMember(group: Group, user_id: int) -> bool:
    return any(m.user_id == user_id for m in group.members)

def isGroupAdmin(group: Group, user_id: int) -> bool:
    for member in group.members:
        if member.user_id == user_id:
            return True
    return False

def isGroupExpensesResolved(group: Group) -> bool:
    # TODO: This will need to be fleshed out
    return True

@app.route("/groups", methods=["GET"])
def get_groups_api():
    current_user = get_user_current()
    with db.get_session() as session:
        # Subquery to get distinct group_id values for a given user_id
        subquery = session.query(GroupMember.group_id.distinct()).filter(GroupMember.user_id == current_user.id)
        # Main query to select all columns from 'groups' where id is in the subquery
        groups = session.query(Group).filter(Group.id.in_(subquery)).all()
        return db.get_json_array(groups)

@app.route("/group/<int:groupId>", methods=["GET"])
def get_group_api(groupId: int):
    with db.get_session() as session:
        current_user = get_user_current()
        group: Group = db.get_entry_by_id(Group, groupId, session)
        if not isGroupMember(group, current_user.id):
            abort(401)
        group_tmp = group.get_dict()
        group_tmp['members'] = db.get_json_array(group.members)
    return group_tmp

@app.route("/group", methods=["POST"])
def new_group_api():
    body = request.get_json()
    new_group = Group(**body)
    return db.add_object(new_group)

@app.route("/group/<int:groupId>", methods=["DELETE"])
def delete_group_api(groupId: int):
    with db.get_session() as session:
        current_user = get_user_current()
        group: Group = db.get_entry_by_id(Group, groupId, session)
        if not isGroupAdmin(group, current_user.id):
            abort(401)
        return db.delete_object(group, session)

@app.route("/group/<int:groupId>/members", methods=["GET"])
def get_group_members_api(groupId: int):
    with db.get_session() as session:
        current_user = get_user_current()
        group: Group = db.get_entry_by_id(Group, groupId, session)
        if not isGroupMember(group, current_user.id):
            abort(401)
        return db.get_json_array(group.members)

@app.route("/group/<int:groupId>/member", methods=["POST"])
def new_group_member_api(groupId: int):
    body = request.get_json()
    with db.get_session() as session:
        new_group_member = GroupMember(**body)
        current_user = get_user_current()
        group: Group = db.get_entry_by_id(Group, groupId, session)
        if not isGroupAdmin(group, current_user.id):
            abort(401)
        return db.add_object(new_group_member)

@app.route("/group/<int:groupId>/member/<int:memberId>", methods=["PATCH"])
def update_group_member_api(groupId: int, memberId: int):
    body = request.get_json()
    with db.get_session() as session:
        current_user = get_user_current()
        group: Group = db.get_entry_by_id(Group, groupId, session)
        if not isGroupAdmin(group, current_user.id):
            abort(401)
        group_member = db.get_entry_by_id(GroupMember, memberId, session)
        return db.update_object_properties(group_member, body)

@app.route("/group/<int:groupId>/member/<int:memberId>", methods=["DELETE"])
def delete_group_member_api(groupId: int, memberId: int):
    with db.get_session() as session:
        current_user = get_user_current()
        group: Group = db.get_entry_by_id(Group, groupId, session)
        if not isGroupAdmin(group, current_user.id):
            abort(401)
        group_member: GroupMember = db.get_entry_by_id(GroupMember, memberId, session)
        if group_member.id == memberId:
            logging.error("Cannot remove self from group")
            abort(401)
        return db.delete_object(group_member)
