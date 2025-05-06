"""Handling Reading and Storing Data.To be replaced with DataBase.
                    load_data(), save_data() """

import json
from logic.models import User, Card, Income, Expense, BudgetCategory, Transaction

def load_user_data(file_path):
    """
    Loads User fron Json File
    :param file_path: path to json file
    :return: User object
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            user = User(data["user_id"])

            user.cards = [Card(**c) for c in data.get("cards", [])]
            user.income = [Income(**i) for i in data.get("income", [])]
            user.recurring_expenses = [Expense(**e) for e in data.get("recurring_expenses", [])]
            user.budget_categories = {}
            for b in data.get("budget_categories", []):
                category = BudgetCategory(b["name"], b["monthly_limit"])
                category.spent = b.get("spent", 0)
                user.budget_categories[category.name] = category
            user.transactions = [Transaction.from_dict(t) for t in data.get("transactions", [])]
            user.savings = data.get("savings", {"goal": 0, "current": 0})

            return user
    except FileNotFoundError:
        return User("default_user")

def save_user_data(user, file_path):
    """
    Saves User to Json File
    :param user: User object
    :param file_path: path to json file
    :return: None
    """
    try:
        try:
            with open(file_path, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            # If the file doesn't exist, initialize with an empty "users" structure
            existing_data = {"users": {}}

        # Convert the current user's data to a dictionary
        user_data = user.to_dict()
        user_id = user_data["user_id"]

        # Check if the user already exists and preserve the "password" field
        if user_id in existing_data.get("users", {}):
            existing_user_data = existing_data["users"][user_id]
            if "password" in existing_user_data:
                user_data["password"] = existing_user_data["password"]

        # Update or add the specified user's data in the "users" section
        existing_data["users"][user_id] = user_data

        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=4)

    except Exception as e:
        print(f"An error occurred while saving data for user_id '{user.user_id}': {e}")