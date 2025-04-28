"""
    Class handles Reset for User at end of month. Used in Savings and Dashboard
"""

from datetime import datetime
from storage import save_user_data


class MonthResetter:

    @staticmethod
    def reset_user_for_new_month(user):
        """Reset budgets, expenses, and month info after month-end."""

        # 1. Reset Budget Categories
        for category in user.budget_categories.values():
            category.spent = 0

        # 2. Clear regular expenses (not recurrent)
        user.transactions.clear()

        # 3. Update month info
        user.last_saved_month = datetime.now().month

        # 4. Save changes
        save_single_user(user)

