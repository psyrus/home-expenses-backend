from flask import request
from ..app import app
from ..models.models import Expense
from ..utils import db
from ..utils.authorization import login_required

@app.route("/expense", methods=["POST"])
@login_required
def add_expense_api():
    body = request.get_json()
    new_expense = Expense(**body)
    return db.add_object(new_expense)


@app.route("/expenses", methods=["GET"])
@login_required
def get_expense_all_api():
    return db.get_json_array(db.get_entries(Expense))


@app.route("/expense/<int:expenseId>", methods=["GET"])
@login_required
def get_expense_api(expenseId):
    return db.get_entry_by_id(Expense, expenseId).get_dict()


@app.route("/expense/<int:expenseId>", methods=["PATCH"])
@login_required
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
@login_required
def remove_expense_api(expenseId):
    expense =  db.get_entry_by_id(Expense ,expenseId)
    return db.delete_object(expense)
