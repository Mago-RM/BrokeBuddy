"""
    Class handles Reset for User at end of month. Used in Savings and Dashboard
"""
from datetime import datetime
from logic.auth import save_single_user

class MonthResetter:

    @staticmethod
    def archive_and_reset_user(user):
        """
        Archive the current month and prepare user for new month.
        :param user: User object
        :return: None
        """

        # 1. Archive current month
        month_name = datetime.now().strftime("%B %Y")  # "April 2025"

        user.monthly_history[month_name] = {
            "budget_summary": {cat.name: cat.spent for cat in user.budget_categories.values()},
            "savings_progress": {
                "goal": user.savings.get("goal", 0),
                "current": user.savings.get("current", 0)
            },
            "total_transactions": len(user.transactions)
        }

        # 2. Reset budgets
        for cat in user.budget_categories.values():
            cat.spent = 0

        # 3. Clear transactions for the new month
        user.transactions.clear()

        # 4. Update last_saved_month
        user.last_saved_month = datetime.now().month

        # 5. Save changes
        save_single_user(user)
