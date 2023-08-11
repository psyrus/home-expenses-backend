from ..app import app

# Group members

@app.route("/group/<int:id>/members", methods=["GET"])
def get_group_members(id):
    return "get group members for group %s" % id

@app.route("/group/<int:id>/members/add", methods=["PATCH"])
def add_group_members(id):
    return "Add members for group %s" % id

@app.route("/group/<int:id>/members/remove", methods=["PATCH"])
def remove_group_members(id):
    return "Remove members for group %s" % id
