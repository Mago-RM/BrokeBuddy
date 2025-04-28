
"""Frame Allows Users to log in their expenses and updated the budget. Visible on Dashboard. """

#Imports
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from datetime import date as dt_date, datetime
from logic.auth import save_single_user
from logic.models import Transaction


class ExpensesFrame(ctk.CTkFrame):
    #Set Up View
    def __init__(self, master, switch_to):
        super().__init__(master)
        self.switch_to = switch_to
        self.current_user = None

        self.configure(fg_color="#4CAF50")

        self.container = ctk.CTkFrame(self, fg_color="#4CAF50", corner_radius=15)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.95)

        self.container.grid_columnconfigure(0, weight=0)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_rowconfigure(1, weight=1)

        logo_and_labels = ctk.CTkFrame(self.container, fg_color="#4CAF50")
        logo_and_labels.grid(row=0, column=0, columnspan=2, sticky="n", pady=(20, 0))

        # Logo on the left of title/summary
        try:
            from PIL import Image, ImageTk
            image = Image.open("assets/cute_doge_circle.png").resize((80, 80))
            self.logo = ImageTk.PhotoImage(image)
            logo_label = tk.Label(logo_and_labels, image=self.logo, bg="#4CAF50")
            logo_label.pack(side="left", padx=(0, 20))
        except:
            print("Logo not found.")

        #Container
        label_container = ctk.CTkFrame(logo_and_labels, fg_color="#4CAF50")
        label_container.pack(side="left", anchor="center")

        self.title = ctk.CTkLabel(label_container, text="Let's Track Your Expenses", font=("Arial Rounded MT Bold", 24),
                                  text_color="white")
        self.title.pack(anchor="w")

        self.summary_label = ctk.CTkLabel(label_container, text="", font=("Arial", 14), text_color="white")
        self.summary_label.pack(anchor="w")

        self.inner_container = ctk.CTkFrame(self.container, fg_color="#4CAF50")
        self.inner_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)

        self.expenses_container = ctk.CTkScrollableFrame(self.inner_container, fg_color="white", corner_radius=10)
        self.inner_container.grid_rowconfigure(0, weight=1)

        self.inner_container.grid_columnconfigure(0, weight=1)
        self.inner_container.grid_rowconfigure(0, weight=1)
        self.expenses_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=(10, 0))

        self.button_frame = ctk.CTkFrame(self.inner_container, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, pady=10)

        self.add_button = ctk.CTkButton(self.button_frame, text="➕ Add Expense",
                                        command=self.open_add_expense_popup)
        self.add_button.pack(side="left", padx=10)

        self.back_button = ctk.CTkButton(self.button_frame, text="⬅ Back", command=self.back_to_dashboard)
        self.back_button.pack(side="left", padx=10)

    def set_user(self, user):
        self.current_user = user
        self.render_expenses()

    def render_expenses(self):
        """Loads expenses for user if they exist"""
        for widget in self.expenses_container.winfo_children():
            widget.destroy()

        if not self.current_user.transactions:
            ctk.CTkLabel(self.expenses_container, text="No expenses recorded yet.", font=("Arial", 14)).pack(pady=20)
            return

        for idx, trans in enumerate(self.current_user.transactions):
            frame = ctk.CTkFrame(self.expenses_container, fg_color="#FFF3E0", border_color="#FB8C00", border_width=2,
                                 corner_radius=12)
            frame.pack(padx=10, pady=10, fill="x")

            label = f"🧾 {trans.name} - ${trans.amount:.2f}"
            ctk.CTkLabel(frame, text=label, font=("Arial Rounded MT Bold", 16), text_color="black").pack(anchor="w",
                                                                                                         padx=15,
                                                                                                         pady=(10, 2))

            ctk.CTkLabel(frame, text=f"Paid with: {trans.payment_method}", font=("Arial", 13), text_color="gray").pack(
                anchor="w", padx=15)
            ctk.CTkLabel(frame, text=f"Category: {trans.category}", font=("Arial", 13), text_color="gray").pack(
                anchor="w", padx=15)
            ctk.CTkLabel(frame, text=f"Date: {trans.date}", font=("Arial", 12), text_color="#5D4037").pack(anchor="w",
                                                                                                         padx=15)

            action_frame = ctk.CTkFrame(frame, fg_color="transparent")
            action_frame.pack(anchor="e", padx=10, pady=10)

            ctk.CTkButton(action_frame, text="Edit", width=60, command=lambda i=idx: self.edit_expense(i)).pack(
                side="left", padx=5)
            ctk.CTkButton(action_frame, text="Delete", width=60, fg_color="red",
                          command=lambda i=idx: self.delete_expense(i)).pack(side="left", padx=5)

    def open_add_expense_popup(self):
        """Adds new expense record. Opens a new popup window."""
        popup = ctk.CTkToplevel(self)
        popup.title("Add Expense")
        popup.geometry("360x600")
        popup.transient(self)
        popup.grab_set()

        ctk.CTkLabel(popup, text="Add Expense", font=("Arial Rounded MT Bold", 20)).pack(pady=(20, 10))

        # Name Entry
        name_entry = ctk.CTkEntry(popup, placeholder_text="Expense Name (e.g., Sushi, Groceries)")
        name_entry.pack(pady=10, padx=20, fill="x")

        # Amount Entry
        amount_entry = ctk.CTkEntry(popup, placeholder_text="Amount (e.g., 35.50)")
        amount_entry.pack(pady=10, padx=20, fill="x")

        # Debug prints
        print("Payment Methods Available:", self.get_account_and_card_names())
        print("Budget Categories Available:", list(self.current_user.budget_categories.keys()))

        # Payment Method
        ctk.CTkLabel(popup, text="Select Payment Method:", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        payment_var = tk.StringVar()
        payment_dropdown = ctk.CTkOptionMenu(popup, variable=payment_var, values=self.get_account_and_card_names())
        payment_dropdown.pack(pady=5, padx=20, fill="x")

        # Budget Category
        ctk.CTkLabel(popup, text="Select Budget Category:", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        category_var = tk.StringVar()
        category_dropdown = ctk.CTkOptionMenu(popup, variable=category_var,
                                              values=list(self.current_user.budget_categories.keys()))
        category_dropdown.pack(pady=5, padx=20, fill="x")

        # Optional Note
        note_entry = ctk.CTkEntry(popup, placeholder_text="Optional Note (e.g., Birthday Dinner)")
        note_entry.pack(pady=10, padx=20, fill="x")

        # Buttons
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(pady=20)

        def save():
            try:
                name = name_entry.get().strip()
                amount = float(amount_entry.get())
                payment_method = payment_var.get()
                category_name = category_var.get()
                note_text = note_entry.get().strip()

                #Checker
                if not name or not payment_method or not category_name:
                    messagebox.showerror("Missing Info", "Please fill out Name, Payment Method, and Category.")
                    return

                today = datetime.now().strftime("%Y-%m-%d")

                # Find the payment method (card)
                payment_obj = self.find_account_or_card_by_name(payment_method)
                if not payment_obj:
                    messagebox.showerror("Error", "Payment method not found.")
                    return

                # Deduct from card balance
                payment_obj.balance -= amount

                # Update budget category spent
                category = self.current_user.budget_categories.get(category_name)
                if category:
                    category.add_expense(amount)

                # Create new Transaction
                new_transaction = Transaction(
                    name=name,
                    amount=amount,
                    payment_method=payment_method,
                    category=category_name,
                    date=today,
                    note=note_text
                )

                # Add to user's transactions
                self.current_user.transactions.append(new_transaction)

                # Save user
                save_single_user(self.current_user)

                # Reset input fields
                name_entry.delete(0, "end")
                amount_entry.delete(0, "end")
                payment_var.set("")
                category_var.set("")
                note_entry.delete(0, "end")

                #Show success message
                messagebox.showinfo("Success", "Expense added successfully!")

                # CHECK ONLY THE CATEGORY JUST UPDATED FOR BUDGET OVERSPENDING ALERT!!!!!!!
                if category and category.spent > category.monthly_limit:
                    warning_msg = f"⚠️ You have exceeded your budget for {category.name}!\n"
                    warning_msg += f"Limit: ${category.monthly_limit:.2f}\nSpent: ${category.spent:.2f}"
                    messagebox.showwarning("Budget Exceeded!", warning_msg)

                # Refresh view. Reset Fields for another entry
                self.render_expenses()

                # Close popup disable to allow consecutive entries
                #popup.destroy()

            except ValueError:
                messagebox.showerror("Invalid Input", "Amount must be a number.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def cancel():
            popup.destroy()

        ctk.CTkButton(button_frame, text="💾 Save", command=save, width=100).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="❌ Cancel", command=cancel, width=100, fg_color="gray").pack(side="left",
                                                                                                      padx=10)

    def edit_expense(self, index):
        """Allows User to edit a transaction posted"""
        trans = self.current_user.transactions[index]

        popup = ctk.CTkToplevel(self)
        popup.title("Edit Transaction")
        popup.geometry("360x500")
        popup.transient(self)
        popup.grab_set()

        name_entry = ctk.CTkEntry(popup)
        name_entry.insert(0, trans.name)
        name_entry.pack(pady=5, padx=20, fill="x")

        amount_entry = ctk.CTkEntry(popup)
        amount_entry.insert(0, str(trans.amount))
        amount_entry.pack(pady=5, padx=20, fill="x")

        payment_var = tk.StringVar(value=trans.payment_method)
        payment_dropdown = ctk.CTkOptionMenu(popup, variable=payment_var, values=self.get_account_and_card_names())
        payment_dropdown.pack(pady=5, padx=20, fill="x")

        category_var = tk.StringVar(value=trans.category)
        category_dropdown = ctk.CTkOptionMenu(popup, variable=category_var,
                                              values=list(self.current_user.budget_categories.keys()))
        category_dropdown.pack(pady=5, padx=20, fill="x")

        def save_changes():
            try:
                new_amount = float(amount_entry.get())
                if new_amount <= 0:
                    raise ValueError("Amount must be positive")

                new_payment = payment_var.get()
                new_category = category_var.get()

                # Step 1: Rollback old values
                old_payment_obj = self.find_account_or_card_by_name(trans.payment_method)
                if old_payment_obj:
                    old_payment_obj.balance += trans.amount  # refund old amount

                old_category = self.current_user.budget_categories.get(trans.category)
                if old_category:
                    old_category.spent -= trans.amount
                    old_category.spent = max(0, old_category.spent)

                # Step 2: Apply new values
                new_payment_obj = self.find_account_or_card_by_name(new_payment)
                if new_payment_obj:
                    new_payment_obj.balance -= new_amount

                new_category_obj = self.current_user.budget_categories.get(new_category)
                if new_category_obj:
                    new_category_obj.spent += new_amount

                # Step 3: Update transaction fields
                trans.name = name_entry.get()
                trans.amount = new_amount
                trans.payment_method = new_payment
                trans.category = new_category

                save_single_user(self.current_user)
                self.render_expenses()
                popup.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(popup, text="💾 Save Changes", command=save_changes).pack(pady=15)

    def delete_expense(self, index):
        """Allows user to delete a transaction posted"""
        confirm = messagebox.askyesno("Confirm", "Delete this transaction?")
        if confirm:
            trans = self.current_user.transactions[index]

            # Rollback balance
            payment_obj = self.find_account_or_card_by_name(trans.payment_method)
            if payment_obj:
                payment_obj.balance += trans.amount

            # Rollback category spent
            category = self.current_user.budget_categories.get(trans.category)
            if category:
                category.spent -= trans.amount
                category.spent = max(0, category.spent)

            self.current_user.transactions.pop(index)
            save_single_user(self.current_user)
            self.render_expenses()

    #Helpers
    def get_account_and_card_names(self):
        names = []
        for card in self.current_user.cards:
            names.append(card.name)
        return names

    def find_account_or_card_by_name(self, name):
        for card in self.current_user.cards:
            if card.name == name:
                return card
        return None

    #End View
    def back_to_dashboard(self):
        """Switches back to Dashboard."""
        self.switch_to("dashboard", user=self.current_user)
