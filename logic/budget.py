'''
    Calculating Functions
'''
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def convert_due_date_input(mmdd: str) -> str:
    """
    Converts a due date string in MM/DD format to a standardized YYYY-MM-DD string format. The year is
    assumed to be the current calendar year. If the input is invalid, an empty string is returned.
    """
    try:
        month, day = map(int, mmdd.split("/"))
        year = datetime.now().year
        due_date = datetime(year, month, day)
        return due_date.strftime("%Y-%m-%d")
    except ValueError:
        return ""

def update_due_dates(user):
    """
    Updates the due dates of recurring expenses for a user.
    It adjusts the due date by adding the appropriate time delta (weekly,
    bi-weekly, or monthly) until the due date is greater than or equal to
    the current date.
    """
    today = datetime.today().date()

    for exp in user.recurring_expenses:
        if not exp.due_date:
            continue
        try:
            due = datetime.strptime(exp.due_date, "%Y-%m-%d").date()
        except ValueError:
            continue

        while due < today:
            if exp.frequency == "weekly":
                due += timedelta(days=7)
            elif exp.frequency == "bi-weekly":
                due += timedelta(days=14)
            elif exp.frequency == "monthly":
                due += relativedelta(months=1)
            else:
                break

        exp.due_date = due.strftime("%Y-%m-%d")