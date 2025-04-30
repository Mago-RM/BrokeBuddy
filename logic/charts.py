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
