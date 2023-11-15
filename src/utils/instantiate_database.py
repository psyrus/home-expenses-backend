import string
import random
from datetime import datetime
from ..models.models import *
from ..utils import db

def get_random_string(len: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(len))

def user() -> dict:
    return {
        "auth_provider_id": get_random_string(15),
        "username": (name:=get_random_string(5)).capitalize(),
        "email": f"{name}@email.com",
        "created_at": str(datetime.now())
        }

def expense(user:int, category:int) -> dict:
    return {
        "registered_by_user": user,
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now()),
        "category": category,
        "expense_date": str(datetime.now()),
        "cost": random.randint(100, 10000),
        "description": get_random_string(random.randint(50, 200)),
        "paid_back": False
    }

def group() -> dict:
    return {
        "name": get_random_string(10),
        "description": get_random_string(random.randint(50, 200))
    }

def groupmember(group: int, user: int, admin: bool) -> dict:
    return {
        "user_id": user,
        "group_id": group,
        "is_admin": admin,
    }

def create_groups(users: list[User]):
    groups: list[Group] = []
    num_groups = len(users) // 3

    for _ in range(num_groups):
        groups.append(Group(**(group())))
        
    db.add_object_list(groups)
    groups = db.get_entries(Group)

    for g in groups:
        num_users = random.randint(1, 8)
        usr_idx = random.randint(0, len(users) // num_users)
        members = []
        while usr_idx < len(users):
            usr = users[usr_idx]
            members.append(GroupMember(**(groupmember(g.id, usr.id, (len(members) < 1)))))
            usr_idx += random.randint(0, len(users) // num_users)

        db.add_object_list(members)


def create_users(count: int):
    for i in range(count):
        params = user()
        db.add_object(User(**params))
    return db.get_entries(User)

def create_expenses(count: int, user_count: int, category_count: int):
    for i in range(count):
        params = expense(random.randint(1, user_count), random.randint(1, category_count))
        db.add_object(Expense(**params))
    return db.get_entries(Expense)

def create_categories():
    categories = ["Kid", "Health", "Home", "Other"]
    for i in range(len(categories)):
        params = {"name": categories[i]}
        db.add_object(Category(**params))
    return db.get_entries(Category)

def add_test_entries():
    users = create_users(20)
    categories = create_categories()
    expenses = create_expenses(100, len(users), len(categories))
    groups = create_groups(users)

if __name__ == "__main__":
    add_test_entries()
