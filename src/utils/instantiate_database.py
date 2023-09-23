import string
import random
from datetime import datetime
from ..models.models import *
# from .api_helpers import add_object_to_database, get_db_entries
from ..utils import db

def get_random_string(len: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(len))

def user(id:int=random.randint(10, 1000)) -> dict:
    return {
        "id": id,
        "auth_provider_id": get_random_string(15),
        "username": (name:=get_random_string(5)).capitalize(),
        "email": f"{name}@email.com",
        "created_at": str(datetime.now())
        }

def expense(id:int, user:int=1, category:int=1) -> dict:
    return {
        "id": id,
        "registered_by_user": user,
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now()),
        "category": category,
        "expense_date": str(datetime.now()),
        "cost": random.randint(100, 10000),
        "description": get_random_string(200),
        "paid_back": False
    }

def create_users(count: int):
    for i in range(count):
        params = user(i+1)
        db.add_object(User(**params))
    return db.get_entries(User)

def create_expenses(count: int, user_count: int, category_count: int):
    for i in range(count):
        params = expense(i+1, random.randint(1, user_count - 1), random.randint(1, user_count - 1))
        db.add_object(Expense(**params))
    return db.get_entries(Expense)

def create_categories():
    categories = ["Kid", "Health", "Home", "Other"]
    for i in range(len(categories)):
        params = {"id": i+1, "name": categories[i]}
        db.add_object(Category(**params))
    return db.get_entries(Category)

def add_test_entries():
    users = create_users(4)
    categories = create_categories()
    expenses = create_expenses(100, len(users), len(categories))

if __name__ == "__main__":
    add_test_entries()
