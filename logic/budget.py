'''
    Calculating Functions
'''

def get_remaining_budget(category):
    """Returns the remaining amount in a budget category."""
    return category.monthly_limit - category.spent

def get_total_budget_summary(user):
    """Returns (total_limit, total_spent, remaining) for all categories."""
    total_limit = sum(cat.monthly_limit for cat in user.budget_categories.values())
    total_spent = sum(cat.spent for cat in user.budget_categories.values())
    remaining = total_limit - total_spent
    return total_limit, total_spent, remaining

def get_over_budget_categories(user):
    """Returns a list of categories where spending exceeded the limit."""
    return [cat for cat in user.budget_categories.values() if cat.spent > cat.monthly_limit]

def record_transaction(user, transaction):
    """Adds a transaction and updates its budget category's spent value."""
    user.transactions.append(transaction)
    category = user.budget_categories.get(transaction.category)
    if category:
        category.add_expense(transaction.amount)