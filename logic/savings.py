def calculate_estimated_savings_for_user(user):
    income = sum(i.amount if i.type == "monthly" else i.amount * 4 for i in user.income)
    credit_due = sum(abs(c.balance) * 0.1 for c in user.cards if c.type == "credit")

    actual_exp = sum(e.amount if e.frequency == "monthly" else e.amount * 4 for e in user.recurring_expenses)
    budgeted_exp = sum(cat.monthly_limit for cat in user.budget_categories.values())

    actual_savings = max(0, income - actual_exp - credit_due)
    budget_savings = max(0, income - budgeted_exp - credit_due)

    return actual_savings, budget_savings
