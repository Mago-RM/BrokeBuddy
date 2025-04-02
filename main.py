
from logic.storage import load_user_data, save_user_data

user = load_user_data("data.json")

# Test reading data
print("User ID:", user.user_id)
for card in user.cards:
    print("Card:", card.name, "| Balance:", card.balance)

# Add a new transaction
from logic.models import Transaction
new_txn = Transaction(amount=25, category="Coffee", note="Coffee")
user.transactions.append(new_txn)

# Save the updated data
save_user_data(user, "data.json")

print("\nIncome Sources:")
for i in user.income:
    print(f"- {i.source}: ${i.amount} ({i.frequency})")

print("\nRecurring Expenses:")
for e in user.recurring_expenses:
    print(f"- {e.name}: ${e.amount} [{e.category}]")

print("\nBudget Categories:")
for b in user.budget_categories:
    print(f"- {b.name}: Spent ${b.spent} / ${b.monthly_limit}")

print("\nTransactions:")
for t in user.transactions:
    print(f"- {t.date} | {t.category}: ${t.amount} ({t.note})")

print("\nSavings:")
print(f"Goal: ${user.savings['goal']} | Current: ${user.savings['current']}")

