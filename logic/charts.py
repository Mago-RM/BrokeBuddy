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

def generate_savings_chart(user):
    """
    Generates a pie chart that visualizes the user's savings progress by comparing
    current savings to the savings goal.
    """
    # Check for missing or invalid savings data
    if not user.savings or "current" not in user.savings or "goal" not in user.savings:
        print("Savings data missing — showing fallback chart.")
        fig, ax = plt.subplots(figsize=(5, 3), dpi=100, constrained_layout=True)
        ax.set_title("No Savings Data Available", fontsize=12)
        ax.axis("off")
        return fig

    current_savings = user.savings["current"]
    goal = user.savings["goal"]
    remaining_goal = max(0, goal - current_savings)

    # If both values are 0, skip pie to avoid divide-by-zero
    if current_savings == 0 and remaining_goal == 0:
        print("Savings and goal are both zero — showing fallback chart.")
        fig, ax = plt.subplots(figsize=(5, 3), dpi=100, constrained_layout=True)
        ax.set_title("No Savings Progress Yet", fontsize=12)
        ax.axis("off")
        return fig

    data = [current_savings, remaining_goal]
    labels = [
        f"Current Savings\n${current_savings}",
        f"Remaining Goal\n${remaining_goal}"
    ]
    colors = ["lightgreen", "lightcoral"]

    fig, ax = plt.subplots(figsize=(5, 3), dpi=100, constrained_layout=True)
    ax.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.set_title("Savings Progress", fontsize=12)

    return fig
