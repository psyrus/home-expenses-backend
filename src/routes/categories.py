from ..app import app
from ..utils import *
from flask import request
from ..models.models import Category


@app.route("/category", methods=["POST"])
def new_category_api():
    body = request.get_json()
    new_category = Category(**body)
    return add_object_to_database(new_category)

@app.route("/categories", methods=["GET"])
def get_categories_api():
    return get_json_array(get_db_entries(Category))

@app.route("/category/<int:id>", methods=["DELETE"])
def delete_category_api(id):
    category =get_db_entry_by_id(Category ,id)
    return delete_object_from_database(category)
