from flask import request
from ..app import app
from ..utils import *
from ..models.models import Expense

# Expense

@app.route("/expense", methods=["POST"])
def add_expense_api():
    body = request.get_json()
    new_expense = Expense(**body)
    return add_object_to_database(new_expense)


@app.route("/expenses", methods=["GET"])
def get_expense_all_api():
    return get_json_array(get_db_entries(Expense))


@app.route("/expense/<int:expenseId>", methods=["GET"])
def get_expense_api(expenseId):
    return get_db_entry_by_id(Expense, expenseId).get_dict()


@app.route("/expense/<int:expenseId>", methods=["PATCH"])
def update_expense_api(expenseId):
    req = request.get_json()
    s = get_session()
    s.begin()
    expense = s.scalars(select(Expense).where(Expense.id == expenseId)).one()
    update_object_properties(expense, req)
    s.commit()
    output = expense.get_dict()
    s.close()
    return output


@app.route("/expense/<int:expenseId>", methods=["DELETE"])
def remove_expense_api(expenseId):
    expense =  get_db_entry_by_id(Expense ,expenseId)
    return delete_object_from_database(expense)
