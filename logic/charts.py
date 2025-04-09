'''
    Graphs for spending, savings, trends, etc
'''
from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd

def generate_category_spending_chart(user):
    data = defaultdict(list)
    for b in user.budget_categories.values():
        data["Category"].append(b.name)
        data["Spending"].append(b.spent)

    df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
    ax.bar(df["Category"], df["Spending"], color="skyblue")
    ax.set_title("Monthly Spending by Category")
    ax.set_ylabel("Amount ($)")
    ax.set_xlabel("Category")
    fig.tight_layout()

    return fig
