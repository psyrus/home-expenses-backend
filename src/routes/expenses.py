from flask import request
from sqlalchemy import select

from ..app import app
from ..models.models import Expense
from ..utils import db

@app.route("/expense", methods=["POST"])
def add_expense_api():
    body = request.get_json()
    new_expense = Expense(**body)
    return db.add_object(new_expense)

@app.route("/expenses", methods=["GET"])
def get_expense_all_api():
    return db.get_json_array(db.get_entries(Expense))

@app.route("/expenses_v2", methods=["GET"])
def get_expense_all_extended_api():
    with db.get_session() as session:
        query = select(Expense)
        extended_expenses = session.scalars(query).all()
        output = []
        for item in extended_expenses:
            json_version = item.get_dict()
            output.append(json_version)
        return output

@app.route("/expense/<int:expenseId>", methods=["GET"])
def get_expense_api(expenseId):
    return db.get_entry_by_id(Expense, expenseId).get_dict()

@app.route("/expense/<int:expenseId>", methods=["PATCH"])
def update_expense_api(expenseId):
    req = request.get_json()
    s = db.get_session()
    s.begin()
    expense = s.scalars(db.select(Expense).where(Expense.id == expenseId)).one()
    db.update_object_properties(expense, req)
    s.commit()
    output = expense.get_dict()
    s.close()
    return output

@app.route("/expense/<int:expenseId>", methods=["DELETE"])
def remove_expense_api(expenseId):
    expense =  db.get_entry_by_id(Expense ,expenseId)
    return db.delete_object(expense)
