import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from datetime import datetime
from logic.charts import generate_category_spending_chart, generate_savings_chart
from logic.auth import save_single_user
from logic.savings import calculate_estimated_savings_for_user
from logic.budget import update_due_dates

class dashFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to):
        super().__init__(master)
        self.current_user = None
        self.switch_to = switch_to

        # Background
        try:
            bg_image = Image.open("assets/money_bg.jpg").resize((1920, 1080))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Background image not found. Check your path.")

        # Main container (grid layout)
        self.container = ctk.CTkFrame(self, fg_color="#4CAF50", corner_radius=15)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.85)
        self.container.grid_rowconfigure((1, 2, 3), weight=1)
        self.container.grid_columnconfigure((0, 1), weight=1)

        # Top row: savings - logo - alerts
        top_frame = ctk.CTkFrame(self.container, fg_color="#4CAF50")
        top_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
        top_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Savings Summary
        self.savings_summary = ctk.CTkFrame(top_frame, fg_color="white", corner_radius=10)
        self.savings_summary.grid(row=0, column=0, padx=10, sticky="nsew")
        ctk.CTkLabel(self.savings_summary, text="💰 Projected Savings", font=("Arial Rounded MT Bold", 14)).pack(pady=(8, 2))
        self.savings_budget_label = ctk.CTkLabel(self.savings_summary, text="", font=("Arial", 12), text_color="green")
        self.savings_budget_label.pack()
        self.savings_actual_label = ctk.CTkLabel(self.savings_summary, text="", font=("Arial", 12), text_color="teal")
        self.savings_actual_label.pack()

        # Logo in the middle
        try:
            image = Image.open("assets/cute_doge_circle.png")
            self.photo = CTkImage(dark_image=image, light_image=image, size=(100, 100))
            ctk.CTkLabel(top_frame, image=self.photo, text="").grid(row=0, column=1, padx=10)
        except FileNotFoundError:
            print("Logo image not found.")

        # Alerts on the right
        self.alert_box = ctk.CTkFrame(top_frame, fg_color="#FFF3E0", border_color="#FB8C00", border_width=2, corner_radius=10)
        self.alert_box.grid(row=0, column=2, padx=10, sticky="nsew")
        self.alert_title = ctk.CTkLabel(self.alert_box, text="⚠️ Upcoming Credit Card Due Dates:", text_color="#E65100", font=("Arial Rounded MT Bold", 14))
        self.alert_title.pack(padx=10, pady=(8, 2), anchor="w")
        self.alert_messages = []

        # Budget Summary
        self.budget_summary = ctk.CTkFrame(self.container, fg_color="white", corner_radius=10)
        self.budget_summary.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.budget_summary, text="🧾 Budget Usage", font=("Arial Rounded MT Bold", 14)).pack(pady=8)
        self.budget_usage_container = ctk.CTkScrollableFrame(self.budget_summary, fg_color="white", corner_radius=10)
        self.budget_usage_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Spending Chart
        self.spending_chart_canvas = tk.Canvas(self.container, bg="white", height=160)
        self.spending_chart_canvas.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Placeholder
        self.placeholder_frame = ctk.CTkFrame(self.container, fg_color="#C8E6C9", corner_radius=10)
        self.placeholder_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.placeholder_frame, text="📦 Future Feature Placeholder", font=("Arial", 12)).pack(pady=15)

        # Recent Expenses
        self.expenses_frame = ctk.CTkFrame(self.container, fg_color="white", corner_radius=10)
        self.expenses_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.expenses_frame, text="🧾 Recent Expenses", font=("Arial", 12)).pack(pady=5)

        # Navigation
        self.nav_bar = ctk.CTkFrame(self, fg_color="#388E3C", corner_radius=0)
        self.nav_bar.pack(side="bottom", fill="x")
        self.create_nav_buttons()

    def set_user(self, user):
        self.current_user = user
        actual, budget = calculate_estimated_savings_for_user(user)
        self.savings_budget_label.configure(text=f"If on budget: ${budget:.2f}")
        self.savings_actual_label.configure(text=f"Actual trend: ${actual:.2f}")

        for widget in self.alert_box.winfo_children():
            if widget != self.alert_title:
                widget.destroy()

        alerts = self.get_upcoming_credit_alerts()
        for name, due_day, days_left in alerts:
            msg = f"• {name} is due in {days_left} day(s) (on the {due_day})"
            ctk.CTkLabel(self.alert_box, text=msg, text_color="#BF360C", font=("Arial", 12)).pack(anchor="w", padx=15, pady=2)

        update_due_dates(user)
        self.show_spending_chart()
        self.render_budget_usage()

        self.update_idletasks()
        self.update()

    def render_budget_usage(self):
        for widget in self.budget_usage_container.winfo_children():
            widget.destroy()

        if not self.current_user.budget_categories:
            ctk.CTkLabel(self.budget_usage_container, text="No budget categories yet.", font=("Arial", 12)).pack(
                pady=10)
            return

        for name, cat in self.current_user.budget_categories.items():
            spent = cat.spent
            limit = cat.monthly_limit
            percent_used = min(spent / limit if limit else 0, 1.0)
            is_over = spent > limit

            # Colors: Green if within budget, red if over limit
            bg_color = "#FFEBEE" if is_over else "#E8F5E9"
            bar_color = "#C62828" if is_over else "#43A047"
            text_color = "#B71C1C" if is_over else "black"
            border_color = "#C62828" if is_over else "#43A047"

            frame = ctk.CTkFrame(self.budget_usage_container, fg_color=bg_color, border_color=border_color,
                                 border_width=2, corner_radius=10)
            frame.pack(padx=10, pady=8, fill="x")

            # Header
            ctk.CTkLabel(frame, text=f"📁 {name}", font=("Arial Rounded MT Bold", 14), text_color=text_color).pack(
                anchor="w", padx=15, pady=(8, 2))
            ctk.CTkLabel(frame, text=f"${spent:.2f} / ${limit:.2f}", font=("Arial", 12), text_color="gray").pack(
                anchor="w", padx=15)

            # Budget usage bar
            bar_container = ctk.CTkFrame(frame, fg_color="#EEEEEE", height=10, corner_radius=5)
            bar_container.pack(padx=15, pady=10, fill="x")

            # Filling of the usage bar
            bar_fill = ctk.CTkFrame(bar_container, fg_color=bar_color, corner_radius=5)
            bar_fill.place(relx=0, rely=0, relheight=1, relwidth=percent_used)

    def show_spending_chart(self):
        for widget in self.spending_chart_canvas.winfo_children():
            widget.destroy()
        fig = generate_category_spending_chart(self.current_user)
        chart_widget = FigureCanvasTkAgg(fig, self.spending_chart_canvas)
        chart_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        chart_widget.draw()

    def get_upcoming_credit_alerts(self):
        today = datetime.now().day
        alerts = []
        for card in self.current_user.cards:
            if card.type == "credit" and card.due_date:
                try:
                    due_day = int(card.due_date)
                    days_until_due = due_day - today
                    if 0 <= days_until_due <= 3:
                        alerts.append((card.name, due_day, days_until_due))
                except ValueError:
                    continue
        return alerts

    def create_nav_buttons(self):
        nav_items = [
            ("Cards", self.open_cards),
            ("Income", self.open_income),
            ("Savings", self.open_savings),
            ("Recurrent", self.open_recurrent),
            ("Expenses", self.open_expenses),
            ("Budget", self.open_budgets),
            ("Trends", self.open_graphs),
            ("Account", self.open_account),
        ]
        for label, action in nav_items:
            ctk.CTkButton(
                self.nav_bar, text=label, fg_color="#4CAF50", text_color="white",
                border_color="white", border_width=2, hover_color="#43a047",
                command=action
            ).pack(side="left", expand=True, fill="x", padx=2, pady=2)

        ctk.CTkButton(
            self.nav_bar, text="EXIT", fg_color="red", text_color="white",
            border_color="white", border_width=2, hover_color="#43a047",
            command=lambda: self.switch_to("login", user=self.current_user)
        ).pack(side="left", padx=2, pady=2)

    def open_income(self): self.switch_to("income", user=self.current_user)
    def open_cards(self): self.switch_to("cards", user=self.current_user)
    def open_savings(self): self.switch_to("savings", user=self.current_user)
    def open_recurrent(self): self.switch_to("recurrent", user=self.current_user)
    def open_expenses(self): self.switch_to("expenses", user=self.current_user)
    def open_budgets(self): self.switch_to("budgets", user=self.current_user)
    def open_graphs(self): self.switch_to("graphs", user=self.current_user)
    def open_account(self): self.switch_to("account", user=self.current_user)
