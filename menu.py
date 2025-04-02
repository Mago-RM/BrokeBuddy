#Console Menu to Test Logic is Working before implementing UI

from logic.storage import load_user_data, save_user_data
from logic.models import Card, Income, Expense, BudgetCategory, Transaction

user = load_user_data("data.json")

def print_main_menu():
    print("\n==== BrokeBuddy Menu ====")
    print("1. View Cards")
    print("2. Add Card")
    print("3. Edit Card")
    print("4. Delete Card")
    print("5. View Income")
    print("6. Add Income")
    print("7. Edit Income")
    print("8. Delete Income")
    print("9. View Expenses")
    print("10. Add Recurring Expense")
    print("11. Edit Recurring Expense")
    print("12. Delete Recurring Expense")
    print("13. View Transactions")
    print("14. Add Transaction")
    print("15. Edit Transaction")
    print("16. Delete Transaction")
    print("17. View Budget Categories")
    print("18. Add Budget Category")
    print("19. Edit Budget Category")
    print("20. Delete Budget Category")
    print("0. Exit")

#                    - - - - - > C A R D S < - - - - - -
def view_cards():
    print("\n-- Cards --")
    for card in user.cards:
        print(f"{card.name}: ${card.balance}")

def add_card():
    name = input("Card name: ")
    balance = float(input("Initial balance: "))
    user.cards.append(Card(name, balance))
    save_user_data(user, "data.json")
    print("Card added!")

def edit_card():
    print("\n-- Edit Card Balance --")
    for i, card in enumerate(user.cards):
        print(f"{i+1}. {card.name}: ${card.balance}")
    choice = int(input("Enter number to edit: ")) - 1
    if 0 <= choice < len(user.cards):
        new_balance = float(input(f"New balance for {user.cards[choice].name}: "))
        user.cards[choice].balance = new_balance
        save_user_data(user, "data.json")
        print("Card updated!")
    else:
        print("Invalid selection.")

def delete_card():
    print("\n-- Delete Card --")
    for i, card in enumerate(user.cards):
        print(f"{i+1}. {card.name} (${card.balance})")
    choice = int(input("Enter number to delete: ")) - 1
    if 0 <= choice < len(user.cards):
        deleted = user.cards.pop(choice)
        save_user_data(user, "data.json")
        print(f"Deleted card: {deleted.name}")
    else:
        print("Invalid selection.")

#                    - - - - - I N C O M E - - - - - -

def view_income():
    print("\n-- Income --")
    for i in user.income:
        print(f"{i.source}: ${i.amount} ({i.frequency})")

def add_income():
    source = input("Income source: ")
    amount = float(input("Amount: "))
    frequency = input("Frequency (monthly/weekly): ")
    user.income.append(Income(source, amount, frequency))
    save_user_data(user, "data.json")
    print("Income added!")

def edit_income():
    print("\n-- Edit Income --")
    for i, inc in enumerate(user.income):
        print(f"{i+1}. {inc.source}: ${inc.amount} ({inc.frequency})")
    choice = int(input("Enter number to edit: ")) - 1
    if 0 <= choice < len(user.income):
        new_amount = float(input("New amount: "))
        new_frequency = input("New frequency (monthly/weekly): ")
        user.income[choice].amount = new_amount
        user.income[choice].frequency = new_frequency
        save_user_data(user, "data.json")
        print("Income updated!")
    else:
        print("Invalid selection.")

def delete_income():
    print("\n-- Delete Income --")
    for i, inc in enumerate(user.income):
        print(f"{i+1}. {inc.source}: ${inc.amount}")
    choice = int(input("Enter number to delete: ")) - 1
    if 0 <= choice < len(user.income):
        deleted = user.income.pop(choice)
        save_user_data(user, "data.json")
        print(f"Deleted income source: {deleted.source}")
    else:
        print("Invalid selection.")

#                    - - - - - E X P E N S E S - - - - - -

def view_expenses():
    print("\n-- Recurring Expenses --")
    for e in user.recurring_expenses:
        print(f"{e.name}: ${e.amount} [{e.category}]")

def add_expense():
    name = input("Expense name: ")
    amount = float(input("Amount: "))
    category = input("Category: ")
    user.recurring_expenses.append(Expense(name, amount, category, recurring=True))
    save_user_data(user, "data.json")
    print("Expense added!")

def edit_expense():
    print("\n-- Edit Recurring Expense --")
    for i, e in enumerate(user.recurring_expenses):
        print(f"{i+1}. {e.name}: ${e.amount} [{e.category}]")
    choice = int(input("Enter number to edit: ")) - 1
    if 0 <= choice < len(user.recurring_expenses):
        new_amount = float(input("New amount: "))
        new_category = input("New category: ")
        user.recurring_expenses[choice].amount = new_amount
        user.recurring_expenses[choice].category = new_category
        save_user_data(user, "data.json")
        print("Expense updated!")
    else:
        print("Invalid selection.")

def delete_expense():
    print("\n-- Delete Recurring Expense --")
    for i, e in enumerate(user.recurring_expenses):
        print(f"{i+1}. {e.name}: ${e.amount} [{e.category}]")
    choice = int(input("Enter number to delete: ")) - 1
    if 0 <= choice < len(user.recurring_expenses):
        deleted = user.recurring_expenses.pop(choice)
        save_user_data(user, "data.json")
        print(f"Deleted expense: {deleted.name}")
    else:
        print("Invalid selection.")


#                    - - - - - T R A N S A C T I O N S - - - - - -

def view_transactions():
    print("\n-- Transactions --")
    for t in user.transactions:
        print(f"{t.date} | {t.category}: ${t.amount} ({t.note})")

def add_transaction():
    amount = float(input("Amount: "))
    category = input("Category: ")
    note = input("Note (optional): ")
    user.transactions.append(Transaction(amount, category, note=note))
    save_user_data(user, "data.json")
    print("Transaction added!")

def edit_transaction():
    print("\n-- Edit Transaction --")
    for i, t in enumerate(user.transactions):
        print(f"{i+1}. {t.date} | {t.category}: ${t.amount} ({t.note})")
    choice = int(input("Enter number to edit: ")) - 1
    if 0 <= choice < len(user.transactions):
        new_amount = float(input("New amount: "))
        new_category = input("New category: ")
        new_note = input("New note (optional): ")
        user.transactions[choice].amount = new_amount
        user.transactions[choice].category = new_category
        user.transactions[choice].note = new_note
        save_user_data(user, "data.json")
        print("Transaction updated!")
    else:
        print("Invalid selection.")

def delete_transaction():
    print("\n-- Delete Transaction --")
    for i, t in enumerate(user.transactions):
        print(f"{i+1}. {t.date} | {t.category}: ${t.amount} ({t.note})")
    choice = int(input("Enter number to delete: ")) - 1
    if 0 <= choice < len(user.transactions):
        deleted = user.transactions.pop(choice)
        save_user_data(user, "data.json")
        print("Deleted transaction.")
    else:
        print("Invalid selection.")

#                    - - - - - B U D G E T  - - - - - -

def view_budgets():
    print("\n-- Budget Categories --")
    for b in user.budget_categories:
        print(f"{b.name}: Spent ${b.spent} / ${b.monthly_limit}")

def add_budget():
    name = input("Category name: ")
    limit = float(input("Monthly limit: "))
    user.budget_categories.append(BudgetCategory(name, limit))
    save_user_data(user, "data.json")
    print("Budget category added!")

def edit_budget():
    print("\n-- Edit Budget Category --")
    for i, b in enumerate(user.budget_categories):
        print(f"{i+1}. {b.name}: Spent ${b.spent} / ${b.monthly_limit}")
    choice = int(input("Enter number to edit: ")) - 1
    if 0 <= choice < len(user.budget_categories):
        new_limit = float(input("New monthly limit: "))
        user.budget_categories[choice].monthly_limit = new_limit
        save_user_data(user, "data.json")
        print("Budget category updated!")
    else:
        print("Invalid selection.")


def delete_budget():
    print("\n-- Delete Budget Category --")
    for i, b in enumerate(user.budget_categories):
        print(f"{i+1}. {b.name} (${b.spent}/${b.monthly_limit})")
    choice = int(input("Enter number to delete: ")) - 1
    if 0 <= choice < len(user.budget_categories):
        deleted = user.budget_categories.pop(choice)
        save_user_data(user, "data.json")
        print(f"Deleted budget: {deleted.name}")
    else:
        print("Invalid selection.")

while True:
    print_main_menu()
    choice = input("Choose an option: ")

    if choice == "1": view_cards()
    elif choice == "2": add_card()
    elif choice == "3": edit_card()
    elif choice == "4": delete_card()
    elif choice == "5": view_income()
    elif choice == "6": add_income()
    elif choice == "7": edit_income()
    elif choice == "8": delete_income()
    elif choice == "9": view_expenses()
    elif choice == "10": add_expense()
    elif choice == "11": edit_expense()
    elif choice == "12": delete_expense()
    elif choice == "13": view_transactions()
    elif choice == "14": add_transaction()
    elif choice == "15": edit_transaction()
    elif choice == "16": delete_transaction()
    elif choice == "17": view_budgets()
    elif choice == "18": add_budget()
    elif choice == "19": edit_budget()
    elif choice == "20": delete_budget()
    elif choice == "0":
        print("Goodbye!")
        break
    else:
        print("Invalid option. Try again.")
