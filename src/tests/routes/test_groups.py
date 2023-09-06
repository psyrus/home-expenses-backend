from ...routes import groups
import unittest

# Need to scaffold a database database for a meaningful test suite...

class TestExpensesRoutes(unittest.TestCase):

    def test_get_groups(self):
        result = groups.get_groups()
        assert (result == "WIP")

    def test_get_group(self):
        result = groups.get_group()
        assert (result == "WIP")
        
    def test_new_group(self):
        result = groups.new_group()
        assert (result == "WIP")