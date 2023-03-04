from ..app import app

# Group

@app.route("/group", methods=["GET"])
def get_groups():
    return "get all groups"

@app.route("/group/<int:id>", methods=["GET"])
def get_group(id):
    return "get group %s" % id

@app.route("/group", methods=["POST"])
def new_group():
    return "create group"

@app.route("/group/<int:id>", methods=["DELETE"])
def delete_group(id):
    return "remove group %s" % id

@app.route("/group/<int:id>", methods=["PATCH"])
def update_group(id):
    return "update group %s" % id