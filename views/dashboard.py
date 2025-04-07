import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from logic.auth import get_user, create_user, delete_user, load_all_users, save_all_users
from logic.models import User

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


#               - - - - - - - > D A S H B O A R D  < - - - - - -
class dashFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to):
        super().__init__(master)
        self.current_user = None
        self.switch_to = switch_to

        try:
            bg_image = Image.open("assets/money_bg.jpg").resize((1920, 1080))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Background image not found. Check your path.")

        self.container = ctk.CTkFrame(self, fg_color="#4CAF50", corner_radius=15)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.25, relheight=0.85)

        self.inner_container = ctk.CTkFrame(self.container, fg_color="#4CAF50")
        self.inner_container.pack(expand=True, fill="both", padx=40, pady=30)

        try:
            #Load Logo
            image = Image.open("assets/doggo_cutout.png")
            self.photo = CTkImage(dark_image=image, light_image=image, size=(200, 200))
            self.image_label = ctk.CTkLabel(self.inner_container, image=self.photo, text="")
            self.image_label.pack(pady=10)
        except FileNotFoundError:
            print("Image not found. Check image path.")

        # Title
        self.title_label = ctk.CTkLabel(
            self.inner_container,
            text="Dashboard Overview",
            font=("Arial Rounded MT Bold", 24),
            text_color="white"
        )
        self.title_label.pack(pady=10)

        # Spending chart placeholder
        self.spending_chart = ctk.CTkLabel(
            self.inner_container,
            text="[Spending Chart Placeholder]",
            width=240,
            height=120,
            fg_color="white",
            text_color="black",
            corner_radius=10
        )
        self.spending_chart.pack(pady=10)

        # Savings progress
        self.savings_progress = ctk.CTkLabel(
            self.inner_container,
            text="[Savings Progress Placeholder]",
            width=240,
            height=60,
            fg_color="white",
            text_color="black",
            corner_radius=10
        )
        self.savings_progress.pack(pady=10)

        #               - - - - - - - > N A V I G A T I O N  ME N U    < - - - - - -

        self.nav_bar = ctk.CTkFrame(self, fg_color="#388E3C", corner_radius=0)
        self.nav_bar.pack(side="bottom", fill="x")

        #CARDS
        self.cards_button = ctk.CTkButton(
            self.nav_bar,
            text="Cards",
            fg_color="#4CAF50",
            text_color="white",
            border_color="white",
            border_width=2,
            hover_color="#43a047",
            command=self.open_cards
        )
        self.cards_button.pack(side="left", expand=True, fill="x", padx=2, pady=2)

        #INCOME
        self.income_button = ctk.CTkButton(
            self.nav_bar,
            text="Income",
            fg_color="#4CAF50",
            text_color="white",
            border_color="white",
            border_width=2,
            hover_color="#43a047",
            command=self.open_income
        )
        self.income_button.pack(side="left", expand=True, fill="x", padx=2, pady=2)

        #SAVINGS
        self.sav_button = ctk.CTkButton(
            self.nav_bar,
            text="Savings",
            fg_color="#4CAF50",
            text_color="white",
            border_color="white",
            border_width=2,
            hover_color="#43a047",
            command=self.open_savings
        )
        self.sav_button.pack(side="left", expand=True, fill="x", padx=2, pady=2)

        # Recurrent
        self.rec_button = ctk.CTkButton(
            self.nav_bar,
            text="Recurrent",
            fg_color="#4CAF50",
            text_color="white",
            border_color="white",
            border_width=2,
            hover_color="#43a047",
            command=self.open_recurrent
        )
        self.rec_button.pack(side="left", expand=True, fill="x", padx=2, pady=2)

        # EXPENSES
        self.exp_button = ctk.CTkButton(
            self.nav_bar,
            text="Expenses",
            fg_color="#4CAF50",
            text_color="white",
            border_color="white",
            border_width=2,
            hover_color="#43a047",
            command=self.open_expenses
        )
        self.exp_button.pack(side="left", expand=True, fill="x", padx=2, pady=2)

        # BUDGET
        self.budget_button = ctk.CTkButton(
            self.nav_bar,
            text="Budget",
            fg_color="#4CAF50",
            text_color="white",
            border_color="white",
            border_width=2,
            hover_color="#43a047",
            command=self.open_budgets
        )
        self.budget_button.pack(side="left", expand=True, fill="x", padx=2, pady=2)

        # Graphs
        self.graph_button = ctk.CTkButton(
            self.nav_bar,
            text="Trends",
            fg_color="#4CAF50",
            text_color="white",
            border_color="white",
            border_width=2,
            hover_color="#43a047",
            command=self.open_graphs
        )
        self.graph_button.pack(side="left", expand=True, fill="x", padx=2, pady=2)

        # Account
        self.acc_button = ctk.CTkButton(
            self.nav_bar,
            text="Account",
            fg_color="#4CAF50",
            text_color="white",
            border_color="white",
            border_width=2,
            hover_color="#43a047",
            command=self.open_account
        )
        self.acc_button.pack(side="left", expand=True, fill="x", padx=2, pady=2)


        self.back_button = ctk.CTkButton(
            self.nav_bar,
            text="EXIT",
            fg_color="red",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=self.back_to_login
        )
        self.back_button.pack(pady=10)

    #               - - - - - - - > A C T I O N S  < - - - - - -
    def set_user(self, user):
        self.current_user = user

    # Graphs, Budgets, Expenses, Recurrent Charges,
    def back_to_login(self):
        self.switch_to("login", user = self.current_user)

    def open_income(self):
        self.switch_to("income", user = self.current_user)

    def open_cards(self):
        self.switch_to("cards", user = self.current_user)

    def open_savings(self):
        self.switch_to("savings", user = self.current_user)

    def open_recurrent(self):
        self.switch_to("recurrent", user = self.current_user)

    def open_expenses(self):
        self.switch_to("expenses", user = self.current_user)

    def open_budgets(self):
        self.switch_to("budgets", user = self.current_user)

    def open_graphs(self):
        self.switch_to("graphs", user = self.current_user)

    def open_account(self):
        self.switch_to("account", user= self.current_user)

