'''
Defining Core Data Classes:
          User, Cards, Income, Expense, Budget Category, Transactions.
'''

from datetime import date

class Card:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def to_dict(self):
        return {
            "name": self.name,
            "balance": self.balance
        }


class Income:
    def __init__(self, source, amount, frequency):
        self.source = source
        self.amount = amount
        self.frequency = frequency  # e.g. 'monthly', 'weekly'

    def to_dict(self):
        return {
            "source": self.source,
            "amount": self.amount,
            "frequency": self.frequency
        }


class Expense:
    def __init__(self, name, amount, category, recurring=False):
        self.name = name
        self.amount = amount
        self.category = category
        self.recurring = recurring

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "category": self.category,
            "recurring": self.recurring
        }


class BudgetCategory:
    def __init__(self, name, monthly_limit):
        self.name = name
        self.monthly_limit = monthly_limit
        self.spent = 0

    def add_expense(self, amount):
        self.spent += amount

    def remaining(self):
        return self.monthly_limit - self.spent

    def to_dict(self):
        return {
            "name": self.name,
            "monthly_limit": self.monthly_limit,
            "spent": self.spent
        }


from datetime import date as dt_date

class Transaction:
    def __init__(self, amount, category, date=None, note=""):
        self.amount = amount
        self.category = category
        self.date = date if date else dt_date.today().isoformat()
        self.note = note

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "note": self.note
        }

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.cards = []
        self.income = []
        self.recurring_expenses = []
        self.budget_categories = []
        self.transactions = []
        self.savings = {"goal": 0, "current": 0}

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "cards": [c.to_dict() for c in self.cards],
            "income": [i.to_dict() for i in self.income],
            "recurring_expenses": [e.to_dict() for e in self.recurring_expenses],
            "budget_categories": [b.to_dict() for b in self.budget_categories],
            "transactions": [t.to_dict() for t in self.transactions],
            "savings": self.savings
        }
