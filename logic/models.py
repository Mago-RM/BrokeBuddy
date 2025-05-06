""" Defining Core Data Classes:
                                 User, Cards, Income, Expense, Budget Category, Transactions."""
from datetime import date as dt_date

class User:
    """Defines a User"""
    def __init__(self, user_id):
        self.user_id = user_id
        self.cards = []
        self.income = []
        self.recurring_expenses = []
        self.budget_categories = {}
        self.transactions = []
        self.savings = {"goal": 0, "current": 0}
        self.savings_accounts = []
        self.monthly_history = {}  # A dictionary to save past history month data

        #Keep track of balances in User for easier reuse
        @property
        def available(self):
            return sum(card.balance for card in self.cards if card.type == "debit")

        @property
        def owe(self):
            return abs(sum(card.balance for card in self.cards if card.type == "credit"))

    def to_dict(self):
        """
        Returns a dictionary representation of the user
        :return: dictionary
        """
        return {
            "user_id": self.user_id,
            "cards": [c.to_dict() for c in self.cards],
            "income": [i.to_dict() for i in self.income],
            "recurring_expenses": [e.to_dict() for e in self.recurring_expenses],
            "budget_categories": [b.to_dict() for b in self.budget_categories.values()],
            "transactions": [t.to_dict() for t in self.transactions],
            "savings": self.savings,
            "savings_accounts": [s.to_dict() for s in self.savings_accounts],
            "monthly_history": self.monthly_history,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a User object from a dictionary
        :param data: dictionary containing user data
        :return: User object
        """
        user = User(user_id=data["user_id"])

        # Load cards
        user.cards = [Card.from_dict(c) for c in data.get("cards", [])]

        # Load income
        user.income = [Income.from_dict(i) for i in data.get("income", [])]

        # Load recurring expenses
        user.recurring_expenses = [Expense.from_dict(e) for e in data.get("recurring_expenses", [])]

        # Load budget categories (important!)
        budget_categories_list = data.get("budget_categories", [])
        user.budget_categories = {
            cat["name"]: BudgetCategory(cat["name"], cat["monthly_limit"]) for cat in budget_categories_list
        }

        # Load transactions
        user.transactions = [Transaction.from_dict(t) for t in data.get("transactions", [])]

        # Load savings
        user.savings = data.get("savings", {"goal": 0, "current": 0})

        # Load savings accounts
        user.savings_accounts = [SavingsAccount.from_dict(sa) for sa in data.get("savings_accounts", [])]

        user.monthly_history = data.get("monthly_history", {})

        return user


class Card:
    """Defines a Card"""
    def __init__(self, name, balance, type="debit", due_date=""):
        self.name = name
        self.balance = balance
        self.type = type  # "debit" or "credit"
        self.due_date = due_date

    def to_dict(self):
        """
        Returns a dictionary representation of the card
        :return: dictionary
        """
        return {
            "name": self.name,
            "balance": self.balance,
            "type": self.type,
            "due_date": self.due_date
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Card object from a dictionary
        :param data: dictionary containing card data
        :return: Card object
        """
        return cls(
            name=data.get("name", ""),
            balance=data.get("balance", 0),
            type=data.get("type", "debit"),
            due_date=data.get("due_date", "")
        )

class Income:
    """Defines an Income"""
    def __init__(self, name, amount, type="one-time", date_added=None):
        self.name = name
        self.amount = amount
        self.type = type  # one-time, weekly, monthly
        self.date_added = date_added

    def to_dict(self):
        """
        Returns a dictionary representation of the income
        :return: dictionary
        """
        return {
            "name": self.name,
            "amount": self.amount,
            "type": self.type,
            "date_added": self.date_added
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates an Income object from a dictionary
        :param data: dictionary containing income data
        :return: Income object
        """
        return cls(
            name=data.get("name", ""),
            amount=data.get("amount", 0.0),
            type=data.get("type", "one-time"),
            date_added=data.get("date_added", None)
        )

class SavingsAccount:
    """Defines a Savings Account"""
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def to_dict(self):
        """
        Returns a dictionary representation of the savings account
        :return: dictionary
        """
        return {
            "name": self.name,
            "amount": self.amount
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates an SavingsAccount object from a dictionary
        :param data: dictionary containing savings account data
        :return: SavingsAccount object
        """
        return cls(
            name=data.get("name", ""),
            amount=data.get("amount", 0.0)
        )

class BudgetCategory:
    """Defines a Budget Category"""
    def __init__(self, name, monthly_limit):
        self.name = name
        self.monthly_limit = monthly_limit
        self.spent = 0

    def add_expense(self, amount):
        """
        Updates amount spent in a budget category based on amount
        :param amount: numeric amount
        :return: None
        """
        self.spent += amount

    def remaining(self):
        """
        Returns remaining amount in a budget category
        :return: numeric amount
        """
        return self.monthly_limit - self.spent

    def to_dict(self):
        """
        Returns a dictionary representation of the budget category
        :return: dictionary
        """
        return {
            "name": self.name,
            "monthly_limit": self.monthly_limit,
            "spent": self.spent
        }

class Transaction:
    """Defines a Transaction"""
    def __init__(self, name, amount, payment_method, category, date=None, note=""):
        self.name = name  # Added
        self.amount = amount
        self.payment_method = payment_method  # Added
        self.category = category
        self.date = date if date else dt_date.today().isoformat()
        self.note = note

    def to_dict(self):
        """
        Returns a dictionary representation of the transaction
        :return: dictionary
        """
        return {
            "name": self.name,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "category": self.category,
            "date": self.date,
            "note": self.note
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Transaction object from a dictionary
        :param data: dictionary containing transaction data
        :return: Transaction object
        """
        return Transaction(
            name=data.get("name", ""),
            amount=data.get("amount", 0.0),
            payment_method=data.get("payment_method", ""),
            category=data.get("category", ""),
            date=data.get("date"),
            note=data.get("note", "")
        )


class Expense:
    """Defines an Recurrent Expense"""
    def __init__(self, name, amount, category, recurring=False, frequency=None, due_date=None, is_membership=False):
        self.name = name
        self.amount = amount
        self.category = category
        self.recurring = recurring
        self.frequency = frequency  # "weekly", "bi-weekly", "monthly"
        self.due_date = due_date    # "MM/DD" string
        self.is_membership = is_membership

    def to_dict(self):
        """
        Returns a dictionary representation of the expense
        :return: dictionary
        """
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
        """
        Creates an Expense object from a dictionary
        :param data: dictionary containing expense data
        :return: Expense object
        """
        return Expense(
            name=data["name"],
            amount=data["amount"],
            category=data.get("category", "misc"),
            recurring=data.get("recurring", False),
            frequency=data.get("frequency"),
            due_date=data.get("due_date"),
            is_membership=data.get("is_membership", False),
        )