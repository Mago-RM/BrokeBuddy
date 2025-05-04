"""
    Graphs for spending, savings, trends, etc
"""

from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

def generate_category_spending_chart(user):
    """
    Generate a bar chart visualizing monthly spending by category from user data.
    """
    data = defaultdict(list)

    for b in user.budget_categories.values():
        data["Category"].append(b.name)
        data["Spending"].append(b.spent)

    # Check if data is empty
    if not data["Category"] or not data["Spending"]:
        print("No category spending data — showing fallback chart.")
        fig, ax = plt.subplots(figsize=(5, 3), dpi=100, constrained_layout=True)
        ax.set_title("No Spending Data Available", fontsize=12)
        ax.axis("off")  # Hide axes for a clean look
        return fig

    # Plot real data
    df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(5, 3), dpi=100, constrained_layout=True)
    ax.bar(df["Category"], df["Spending"], color="skyblue")
    ax.set_title("Your Month So Far", fontsize=12)
    ax.set_ylabel("Amount ($)", fontsize=10)
    ax.set_xlabel("Category", fontsize=10)

    return fig

def generate_monthly_trend_chart(user):
    """Generates Monthly Trend Chart"""
    # Check if monthly_history exists and has data
    monthly_history = user.monthly_history if user and user.monthly_history else {}

    if monthly_history:
        # Use data from monthly_history if available
        months = list(monthly_history.keys())
        spending_data = [
            sum(category for category in month["budget_summary"].values())
            for month in monthly_history.values()
        ]
    else:
        # Uses transaction data if no monthly_history exists
        if not user.transactions:
            # Show empty chart if no transactions exist
            fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
            ax.set_title("No Data Available")
            ax.axis("off")
            return fig

        df = pd.DataFrame([t.to_dict() for t in user.transactions])
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M').astype(str)
        monthly_spending = df.groupby('month')['amount'].sum()

        months = monthly_spending.index.tolist()
        spending_data = monthly_spending.tolist()

    # Generate the chart
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    ax.plot(months, spending_data, marker='o', color='teal', label="Spending")
    for i, v in enumerate(spending_data):
        plt.annotate(f'${v}', (i,v), textcoords="offset points", xytext=(0, 10), ha='center')
    ax.set_title("Monthly Spending Trend")
    ax.set_ylabel("Total Spent ($)")
    ax.set_xlabel("Month")
    ax.grid(True)
    ax.legend()
    return fig
