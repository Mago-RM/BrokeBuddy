import unittest
from datetime import datetime, timedelta
from logic.budget import convert_due_date_input, update_due_dates
from logic.models import User, Expense


class TestBudget(unittest.TestCase):
    def setUp(self):
        self.user = User("testuser")

    def test_convert_due_date_input_valid(self):
        # Test valid date conversion
        test_cases = [
            ("1/15", f"{datetime.now().year}-01-15"),
            ("01/15", f"{datetime.now().year}-01-15"),
            ("12/31", f"{datetime.now().year}-12-31"),
            ("3/1", f"{datetime.now().year}-03-01"),
        ]

        for input_date, expected in test_cases:
            with self.subTest(input_date=input_date):
                result = convert_due_date_input(input_date)
                self.assertEqual(result, expected)

    def test_convert_due_date_input_invalid(self):
        # Test invalid date inputs
        invalid_dates = [
            "13/01",  # Invalid month
            "12/32",  # Invalid day
            "0/1",  # Invalid month
            "1/0",  # Invalid day
            "abc",  # Not a date
            "1-15",  # Wrong format
            "",  # Empty string
        ]

        for invalid_date in invalid_dates:
            with self.subTest(invalid_date=invalid_date):
                result = convert_due_date_input(invalid_date)
                self.assertEqual(result, "")

    def test_update_due_dates_weekly(self):
        # Create a weekly expense with past due date
        past_date = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
        expense = Expense(
            name="Weekly Test",
            amount=10.0,
            category="Test",
            recurring=True,
            frequency="weekly",
            due_date=past_date
        )
        self.user.recurring_expenses = [expense]

        update_due_dates(self.user)

        # The new date should be in the future
        updated_date = datetime.strptime(expense.due_date, "%Y-%m-%d").date()
        self.assertGreaterEqual(updated_date, datetime.now().date())

    def test_update_due_dates_biweekly(self):
        # Create a bi-weekly expense with past due date
        past_date = (datetime.now() - timedelta(days=21)).strftime("%Y-%m-%d")
        expense = Expense(
            name="Bi-weekly Test",
            amount=20.0,
            category="Test",
            recurring=True,
            frequency="bi-weekly",
            due_date=past_date
        )
        self.user.recurring_expenses = [expense]

        update_due_dates(self.user)

        # The new date should be in the future
        updated_date = datetime.strptime(expense.due_date, "%Y-%m-%d").date()
        self.assertGreaterEqual(updated_date, datetime.now().date())

    def test_update_due_dates_monthly(self):
        # Create a monthly expense with past due date
        past_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        expense = Expense(
            name="Monthly Test",
            amount=100.0,
            category="Test",
            recurring=True,
            frequency="monthly",
            due_date=past_date
        )
        self.user.recurring_expenses = [expense]

        update_due_dates(self.user)

        # The new date should be in the future
        updated_date = datetime.strptime(expense.due_date, "%Y-%m-%d").date()
        self.assertGreaterEqual(updated_date, datetime.now().date())

    def test_update_due_dates_invalid_frequency(self):
        # Test expense with invalid frequency
        original_date = "2023-01-01"
        expense = Expense(
            name="Invalid Frequency Test",
            amount=50.0,
            category="Test",
            recurring=True,
            frequency="invalid",
            due_date=original_date
        )
        self.user.recurring_expenses = [expense]

        update_due_dates(self.user)

        # The date should remain unchanged
        self.assertEqual(expense.due_date, original_date)

    def test_update_due_dates_no_due_date(self):
        # Test expense with no due date
        expense = Expense(
            name="No Due Date Test",
            amount=40.0,
            category="Test",
            recurring=True,
            frequency="monthly",
            due_date=None
        )
        self.user.recurring_expenses = [expense]

        # Update due dates should not modify the None due_date
        update_due_dates(self.user)
        self.assertIsNone(expense.due_date)


if __name__ == '__main__':
    unittest.main()