from flask import request
from ..app import app
from ..utils import *
from ..models.models import Expense

# Expense


@app.route("/expenses", methods=["GET"])
def get_expense_all_api():
    return get_json_array(get_db_entries(Expense))


@app.route("/expenses/<int:expenseId>", methods=["GET"])
def get_expense(expenseId):
    return "get expenses with ID %s" % expenseId


@app.route("/expense/<int:expenseId>", methods=["PATCH"])
def update_expense(expenseId):
    return "update expense with ID %s" % expenseId


@app.route("/expense/<int:expenseId>", methods=["DELETE"])
def remove_expense(expenseId):
    return "remove expense with ID %s" % expenseId

@app.route("/expense", methods=["POST"])
def add_expense_api_test():
    body = request.get_json()
    new_expense = Expense(**body)
    return add_object_to_database(new_expense)
