from ..app import app
from flask import request
from ..models.models import Category
from ..utils import db
from ..utils.authorization import login_required


@app.route("/category", methods=["POST"])
@login_required
def new_category_api():
    body = request.get_json()
    new_category = Category(**body)
    return db.add_object(new_category)

@app.route("/categories", methods=["GET"])
@login_required
def get_categories_api():
    return db.get_json_array(db.get_entries(Category))

@app.route("/category/<int:id>", methods=["DELETE"])
@login_required
def delete_category_api(id):
    category = db.get_entry_by_id(Category ,id)
    return db.delete_object(category)
