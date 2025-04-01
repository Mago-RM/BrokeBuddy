'''
Handling Reading and Storing Data.
To be replaced with DataBase.

       load_data(), save_data()
'''
import json
from logic.models import User, Card, Income, Expense, BudgetCategory, Transaction

def load_user_data(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            user = User(data["user_id"])

            user.cards = [Card(**c) for c in data.get("cards", [])]
            user.income = [Income(**i) for i in data.get("income", [])]
            user.recurring_expenses = [Expense(**e) for e in data.get("recurring_expenses", [])]
            user.budget_categories = [BudgetCategory(b["name"], b["monthly_limit"]) for b in data.get("budget_categories", [])]
            for cat, b in zip(user.budget_categories, data.get("budget_categories", [])):
                cat.spent = b.get("spent", 0)
            user.transactions = [Transaction(**t) for t in data.get("transactions", [])]
            user.savings = data.get("savings", {"goal": 0, "current": 0})

            return user
    except FileNotFoundError:
        return User("default_user")

def save_user_data(user, file_path):
    with open(file_path, 'w') as f:
        json.dump(user.to_dict(), f, indent=4)
