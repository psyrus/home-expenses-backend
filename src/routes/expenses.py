from flask import request, abort
from ..app import app
from ..utils import get_session
# Expense


@app.route("/expenses/group/<int:id>", methods=["GET"])
def get_group_expenses_list(id):
    return "get expenses for group %s" % id


@app.route("/expenses/<int:expenseId>", methods=["GET"])
def get_expense(expenseId):
    return "get expenses with ID %s" % expenseId


@app.route("/expenses/group/<int:id>/add", methods=["POST"])
def add_expense(id):
    return "add new expense for group %s" % id


@app.route("/expenses/<int:expenseId>", methods=["PATCH"])
def update_expense(expenseId):
    return "update expense with ID %s" % expenseId


@app.route("/expenses/<int:expenseId>", methods=["DELETE"])
def remove_expense(expenseId):
    return "remove expense with ID %s" % expenseId

@app.route("/expenses/add", methods=["POST"])
def add_expense_api_test():
    request_data = request.get_json()
    print(request_data)
    request_data['extra'] = "Trevor's special sauce"
    return request_data
