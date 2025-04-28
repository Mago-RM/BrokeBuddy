""" Class Handles Graphics View. """

import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from logic.charts import generate_category_spending_chart, generate_savings_chart
import matplotlib.pyplot as plt
import pandas as pd

class GraphsFrame(ctk.CTkFrame):
    #Sets View
    def __init__(self, master, switch_to):
        super().__init__(master)
        self.switch_to = switch_to
        self.current_user = None
        self.configure(fg_color="#4CAF50")

        self.title = ctk.CTkLabel(
            self, text="📊 Spending Trends & Insights",
            font=("Arial Rounded MT Bold", 24),
            text_color="white"
        )
        self.title.pack(pady=20)

        # Scrollable container for charts
        self.chart_container = ctk.CTkScrollableFrame(
            self, fg_color="white", corner_radius=15
        )
        self.chart_container.pack(expand=True, fill="both", padx=40, pady=10)

        self.back_button = ctk.CTkButton(
            self, text="⬅ Back", command=self.back_to_dashboard,
            fg_color="#43A047", text_color="white", hover_color="#388E3C"
        )
        self.back_button.pack(pady=10)

    def set_user(self, user):
        """Set User"""
        self.current_user = user
        self.render_charts()

    def render_charts(self):
        """Loads Charts"""
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        charts = [
            ("📁 Category Spending", generate_category_spending_chart(self.current_user)),
            ("📈 Monthly Spending Trend", self.generate_monthly_trend_chart()),
            ("💰 Savings Progress", generate_savings_chart(self.current_user))
        ]

        for title, fig in charts:
            self.add_chart_widget(title, fig)

    def add_chart_widget(self, title, fig):
        """Adds Chart Widget"""
        chart_frame = ctk.CTkFrame(
            self.chart_container, fg_color="#E8F5E9",
            border_color="#43A047", border_width=2, corner_radius=12
        )
        chart_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(
            chart_frame, text=title, font=("Arial Rounded MT Bold", 16),
            text_color="black"
        ).pack(pady=(10, 0))

        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def generate_monthly_trend_chart(self):
        """Generates Monthly Trend Chart"""
        # Check if monthly_history exists and has data
        monthly_history = self.current_user.monthly_history if self.current_user and self.current_user.monthly_history else {}

        if monthly_history:
            # Use data from monthly_history if available
            months = list(monthly_history.keys())
            spending_data = [
                sum(category for category in month["budget_summary"].values())
                for month in monthly_history.values()
            ]
        else:
            # Uses transaction data if no monthly_history exists
            if not self.current_user.transactions:
                # Show empty chart if no transactions exist
                fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
                ax.set_title("No Data Available")
                ax.axis("off")
                return fig

            df = pd.DataFrame([t.to_dict() for t in self.current_user.transactions])
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.to_period('M').astype(str)
            monthly_spending = df.groupby('month')['amount'].sum()

            months = monthly_spending.index.tolist()
            spending_data = monthly_spending.tolist()

        # Generate the chart
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot(months, spending_data, marker='o', color='teal', label="Spending")
        ax.set_title("Monthly Spending Trend")
        ax.set_ylabel("Total Spent ($)")
        ax.set_xlabel("Month")
        ax.grid(True)
        ax.legend()
        return fig

    def back_to_dashboard(self):
        """Switches back to Dashboard"""
        self.switch_to("dashboard", user=self.current_user)
