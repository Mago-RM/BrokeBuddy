# User Log In Credentials
# Connected to data.json for now.

import json
from logic.models import User, Card, Income, Expense, BudgetCategory, Transaction, SavingsAccount


def create_user(user_id, file_path="data.json"):
    """
    Create a new user by adding it to the specified data file if it does not already exist.

    This function checks whether the user with the given user ID already exists
    in the file specified by `file_path`. If the user does not exist, the function
    prompts for a password and creates a new user entry.

    If the user ID already exists, the function does not create a new user.
    """
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


def get_user(user_id, password_attempt="", file_path="data.json"):
    """
    Retrieves and returns a user object after verifying the password attempt and loading
    the user's data. It validates the given user ID and its password. If the validation
    succeeds, it reconstructs the user's data and returns it as a User object, else None.
    """
    data = load_all_users(file_path)
    if user_id not in data["users"]:
        return None  # User doesn't exist

    saved_password = data["users"][user_id].get("password")

    if password_attempt != saved_password:
        return None  # Password mismatch

    user_data = data["users"][user_id]
    user = User(user_id)
    user.cards = [Card.from_dict(c) for c in user_data.get("cards", [])]
    user.income = [Income(**i) for i in user_data.get("income", [])]
    user.recurring_expenses = [Expense(**e) for e in user_data.get("recurring_expenses", [])]
    user.budget_categories = {}
    user.savings_accounts = [SavingsAccount.from_dict(s) for s in user_data.get("savings_accounts", [])]
    for b in user_data.get("budget_categories", []):
        category = BudgetCategory(b["name"], b["monthly_limit"])
        category.spent = b.get("spent", 0)
        user.budget_categories[category.name] = category
    user.transactions = [Transaction(**t) for t in user_data.get("transactions", [])]
    user.savings = user_data.get("savings", {"goal": 0, "current": 0})

    return user


def delete_user(user_id, file_path="data.json"):
    """
    Delete a user from the data storage.

    This function removes a user identified by their user ID from the specified
    data file. The storage is expected to be in JSON format, containing a "users"
    key mapping user IDs to their data. If the user ID does not exist in the
    storage, prints the message and does nothing.
    """
    data = load_all_users(file_path)
    if user_id in data["users"]:
        del data["users"][user_id]
        save_all_users(data, file_path)
        print("User deleted.")
    else:
        print("User not found.")

def list_users(file_path="data.json"):
    """
    Lists all the user names from a provided JSON file.
    """
    data = load_all_users(file_path)
    return list(data["users"].keys())

def load_all_users(file_path="data.json"):
    """
    Loads all users from the specified JSON file. If the file is not found, it will
    return a dictionary with an empty "users" key.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}}

def save_all_users(data, file_path="data.json"):
    """
    Save user data to a specified JSON file.
    """
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def save_single_user(user: User):
    """
    Saves the updated user data while preserving their password.
    """

    # Load full user database
    all_data = load_all_users()

    # Get original password
    original_user_data = all_data["users"].get(user.user_id, {})
    password = original_user_data.get("password", "")

    # Update and preserve password
    updated_data = user.to_dict()
    updated_data["password"] = password

    # Save back to database
    all_data["users"][user.user_id] = updated_data
    save_all_users(all_data)

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




