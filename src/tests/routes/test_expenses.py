from ...routes import expenses
import unittest
from ...utils import *
from random import randint

'''
Note: This unit test requires the actual database to be up and running.

The database should technically be scaffolded with data before this test is run.
'''

class TestExpensesRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_id = randint(10000, 99999)
        engine_endpoint = get_test_engine_endpoint(cls.test_id)
        cls.engine = get_engine(engine_endpoint)
        reset_db(cls.engine)
        cls.db_session = get_session(cls.engine.url)

    @classmethod
    def tearDownClass(cls):
        print("Removing test database [%s]" % cls.engine.url.render_as_string())
        remove_test_database(cls.engine.url)

    def test_get_expense(self):
        result = expenses.get_expense_api(5)
        assert (result == "get expenses with ID 5")

    # def test_get_expense_all(self):
    #     result = expenses.get_expense_all_api()
    #     assert (result == "failing")

    # def test_remove_expense(expenseId):
    #     result = expenses.remove_expense_api(5)
    #     assert (result == "failing")
