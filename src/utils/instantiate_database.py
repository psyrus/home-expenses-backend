import requests
import json
import string
import random
from datetime import datetime

def get_random_string(len: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(len))

def user(id:int=random.randint(10, 1000)) -> dict:
    return {
        "id": id,
        "auth_provider_id": get_random_string(5),
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
        "description": get_random_string(10),
        "paid_back": False
    }

def create_users(count: int):
    print(f"Creating user: ", end='', flush=True)
    for i in range(count):
        print(f"{i} | ", end='', flush=True)
        res = requests.post("http://localhost:5000/user", json=user(i))
    print("Done")

def create_expenses(count: int):
    print(f"Creating expense: ", end='', flush=True)
    for i in range(count):
        print(f"{i} | ", end='', flush=True)
        res = requests.post("http://localhost:5000/expense", json=expense(i, random.randint(1, 4), random.randint(1, 4)))
    print("Done")

def create_categories():
    res = requests.get("http://localhost:5000/categories")
    if json.loads(res.text):
        return
    categories = ["Kid", "Health", "Home", "Other"]
    print(f"Creating category: ", end='', flush=True)
    for i in range(len(categories)):
        print(f"{i} | ", end='', flush=True)
        requests.post("http://localhost:5000/category", json={"id": i, "name": categories[i]})
    print("Done")

if __name__ == "__main__":
    create_users(4)

    create_categories()

    create_expenses(4)
