from ..app import app
from flask import request
from ..models.models import Category
from ..utils import db


@app.route("/category", methods=["POST"])
def new_category_api():
    body = request.get_json()
    new_category = Category(**body)
    return db.add_object(new_category)

@app.route("/categories", methods=["GET"])
def get_categories_api():
    return db.get_json_array(db.get_entries(Category))

@app.route("/category/<int:id>", methods=["DELETE"])
def delete_category_api(id):
    category = db.get_entry_by_id(Category ,id)
    return db.delete_object(category)
