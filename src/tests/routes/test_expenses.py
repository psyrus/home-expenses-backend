from ...routes import expenses
import unittest


class TestExpensesRoutes(unittest.TestCase):

    def test_get_group_expenses_list(self):
        result = expenses.get_group_expenses_list(5)
        assert (result == "get expenses for group 5")

    def test_get_expense(self):
        result = expenses.get_expense(5)
        assert (result == "get expenses with ID 5")

    def test_add_expense(id):
        result = expenses.add_expense(5)
        assert (result == "add new expense for group 5")

    def test_update_expense(expenseId):
        result = expenses.update_expense(5)
        assert (result == "update expense with ID 5")

    def test_remove_expense(expenseId):
        result = expenses.remove_expense(5)
        assert (result == "remove expense with ID 5")
