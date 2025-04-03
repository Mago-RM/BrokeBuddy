# User Log In Credentials
# Connected to data.json for now.

import json
from logic.models import User, Card, Income, Expense, BudgetCategory, Transaction

def create_user(user_id, file_path="data.json"):
    data = load_all_users(file_path)
    if user_id in data["users"]:
        print("User already exists.")
        return None

    password = input("Choose a password: ") #Simple password for testing. Not Secure

    user = User(user_id)
    user_data = user.to_dict()
    user_data["password"] = password  # store raw password

    data["users"][user_id] = user_data
    save_all_users(data, file_path)

    print("User created!")
    return user


def get_user(user_id, file_path="data.json"):
    data = load_all_users(file_path)
    if user_id not in data["users"]:
        print("User not found.")
        return None

    saved_password = data["users"][user_id].get("password")
    attempt = input("Enter password: ")

    if attempt != saved_password:
        print("Incorrect password.")
        return None

    user_data = data["users"][user_id]
    user = User(user_id)
    user.cards = [Card(**c) for c in user_data.get("cards", [])]
    user.income = [Income(**i) for i in user_data.get("income", [])]
    user.recurring_expenses = [Expense(**e) for e in user_data.get("recurring_expenses", [])]
    user.budget_categories = {}
    for b in user_data.get("budget_categories", []):
        category = BudgetCategory(b["name"], b["monthly_limit"])
        category.spent = b.get("spent", 0)
        user.budget_categories[category.name] = category
    user.transactions = [Transaction(**t) for t in user_data.get("transactions", [])]
    user.savings = user_data.get("savings", {"goal": 0, "current": 0})

    return user


def delete_user(user_id, file_path="data.json"):
    data = load_all_users(file_path)
    if user_id in data["users"]:
        del data["users"][user_id]
        save_all_users(data, file_path)
        print("User deleted.")
    else:
        print("User not found.")

def list_users(file_path="data.json"):
    data = load_all_users(file_path)
    return list(data["users"].keys())

def load_all_users(file_path="data.json"):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}}

def save_all_users(data, file_path="data.json"):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def login_menu():
    while True:
        print("==== BrokeBuddy Login ====")
        print("1. Log In")
        print("2. Create New User")
        print("3. Delete User")
        print("4. List Users")
        print("0. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            user_id = input("Username: ")
            user = get_user(user_id)
            if user:
                return user
        elif choice == "2":
            user_id = input("Choose a username: ")
            user = create_user(user_id)
            if user:
                return user
        elif choice == "3":
            user_id = input("Enter username to delete: ")
            delete_user(user_id)
        elif choice == "4":
            print("\nUsers:")
            for u in list_users():
                print(f"- {u}")
            print("")  # optional space
        elif choice == "0":
            print("Goodbye!")
            exit()
        else:
            print("Invalid choice.")




