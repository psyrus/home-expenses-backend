from ..app import app
from flask import request

# Group


@app.route("/group", methods=["GET"])
def get_groups():
    return "get all groups"

@app.route("/group/<int:id>", methods=["GET"])
def get_group(id):
    return "get group %s" % id


@app.route("/group", methods=["POST"])
def new_group():
    request_data = request.get_json()

    group_name = request_data['group_name']
    
    return "create group %s" % group_name


@app.route("/group/<int:id>", methods=["DELETE"])
def delete_group(id):
    return "remove group %s" % id


@app.route("/group/<int:id>", methods=["PATCH"])
def update_group(id):
    return "update group %s" % id
