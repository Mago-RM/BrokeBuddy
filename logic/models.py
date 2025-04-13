from datetime import date as dt_date

'''
Defining Core Data Classes:
          User, Cards, Income, Expense, Budget Category, Transactions.
'''
class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.cards = []
        self.income = []
        self.recurring_expenses = []
        self.budget_categories = {} # Change to a dict mapping categoryName:budgetObject
        self.transactions = []
        self.savings = {"goal": 0, "current": 0}
        self.savings_accounts = []

        #Keep track of balances in User for easier reuse
        @property
        def available(self):
            return sum(card.balance for card in self.cards if card.type == "debit")

        @property
        def owe(self):
            return abs(sum(card.balance for card in self.cards if card.type == "credit"))

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "cards": [c.to_dict() for c in self.cards],
            "income": [i.to_dict() for i in self.income],
            "recurring_expenses": [e.to_dict() for e in self.recurring_expenses],
            "budget_categories": [b.to_dict() for b in self.budget_categories.values()],
            "transactions": [t.to_dict() for t in self.transactions],
            "savings": self.savings,
            "savings_accounts": [s.to_dict() for s in self.savings_accounts],
        }

class Card:
    def __init__(self, name, balance, type="debit", due_date=""):
        self.name = name
        self.balance = balance
        self.type = type  # "debit" or "credit"
        self.due_date = due_date

    def to_dict(self):
        return {
            "name": self.name,
            "balance": self.balance,
            "type": self.type,
            "due_date": self.due_date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            balance=data.get("balance", 0),
            type=data.get("type", "debit"),
            due_date=data.get("due_date", "")
        )

class Income:
    def __init__(self, name, amount, type="one-time", date_added=None):
        self.name = name
        self.amount = amount
        self.type = type  # one-time, weekly, monthly
        self.date_added = date_added

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "type": self.type,
            "date_added": self.date_added
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            amount=data.get("amount", 0.0),
            type=data.get("type", "one-time"),
            date_added=data.get("date_added", None)
        )

class SavingsAccount:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            amount=data.get("amount", 0.0)
        )

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

class Expense:
    def __init__(self, name, amount, category, recurring=False, frequency=None, due_date=None, is_membership=False):
        self.name = name
        self.amount = amount
        self.category = category
        self.recurring = recurring
        self.frequency = frequency  # "weekly", "bi-weekly", "monthly"
        self.due_date = due_date    # "MM/DD" string
        self.is_membership = is_membership

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "category": self.category,
            "recurring": self.recurring,
            "frequency": self.frequency,
            "due_date": self.due_date,
            "is_membership": self.is_membership,
        }

    @staticmethod
    def from_dict(data):
        return Expense(
            name=data["name"],
            amount=data["amount"],
            category=data.get("category", "misc"),
            recurring=data.get("recurring", False),
            frequency=data.get("frequency"),
            due_date=data.get("due_date"),
            is_membership=data.get("is_membership", False),
        )





