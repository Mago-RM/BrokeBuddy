import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from logic.auth import save_single_user
from logic.models import SavingsAccount

class SavingsFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to):
        super().__init__(master)
        self.switch_to = switch_to
        self.current_user = None

        self.configure(fg_color="#4CAF50")

        # Main container like other frames
        self.container = ctk.CTkFrame(self, fg_color="#4CAF50", corner_radius=15)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.85)

        self.inner_container = ctk.CTkFrame(self.container, fg_color="#4CAF50")
        self.inner_container.pack(expand=True, fill="both", padx=40, pady=30)

        self.title = ctk.CTkLabel(self.inner_container, text="💰 Your Savings", font=("Arial Rounded MT Bold", 24), text_color="white")
        self.title.pack(pady=(0, 10))

        # Estimated savings
        self.label_already_saved = ctk.CTkLabel(self.inner_container, text="", font=("Arial", 14), text_color="white")
        self.label_already_saved.pack(pady=(0, 2))

        self.estimate_label_budget = ctk.CTkLabel(self.inner_container, text="", font=("Arial", 14), text_color="white")
        self.estimate_label_budget.pack(pady=(0, 2))

        self.estimate_label_actual = ctk.CTkLabel(self.inner_container, text="", font=("Arial", 14), text_color="white")
        self.estimate_label_actual.pack(pady=(0, 2))

        self.projected_total_label = ctk.CTkLabel(self.inner_container, text="", font=("Arial Rounded MT Bold", 14), text_color="white")
        self.projected_total_label.pack(pady=(0, 10))

        # Savings list container
        self.savings_container = ctk.CTkScrollableFrame(self.inner_container, fg_color="white", corner_radius=10)
        self.savings_container.pack(expand=True, fill="both", padx=10, pady=10)

        self.button_frame = ctk.CTkFrame(self.inner_container, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.add_button = ctk.CTkButton(self.button_frame, text="➕ Add Savings Account", command=self.open_add_popup)
        self.add_button.pack(side="left", padx=10)

        self.back_button = ctk.CTkButton(self.button_frame, text="⬅ Back", command=self.back_to_dashboard)
        self.back_button.pack(side="left", padx=10)

    def set_user(self, user):
        self.current_user = user
        self.render_savings()

    def get_total_saved(self):
        return sum(acct.amount for acct in self.current_user.savings_accounts)

    def calculate_estimated_savings(self):
        income = sum(i.amount if i.type == "monthly" else i.amount * 4 for i in self.current_user.income)
        credit_due = sum(abs(c.balance) * 0.1 for c in self.current_user.cards if c.type == "credit")

        actual_exp = sum(e.amount if e.type == "monthly" else e.amount * 4 for e in self.current_user.recurring_expenses)
        budgeted_exp = sum(cat.monthly_limit for cat in self.current_user.budget_categories.values())

        actual_savings = max(0, income - actual_exp - credit_due)
        budget_savings = max(0, income - budgeted_exp - credit_due)

        return actual_savings, budget_savings

    def render_savings(self):
        for widget in self.savings_container.winfo_children():
            widget.destroy()

        actual, budget = self.calculate_estimated_savings()
        already_saved = self.get_total_saved()
        projected_actual = already_saved + actual
        projected_budget = already_saved + budget

        self.label_already_saved.configure(text=f"🟢 Already Saved: ${already_saved:.2f}")
        self.estimate_label_budget.configure(text=f"📊 If you stay within your budget: +${budget:.2f}")
        self.estimate_label_actual.configure(text=f"📉 Based on actual spending:       +${actual:.2f}")
        self.projected_total_label.configure(text=f"💰 Projected Total Savings: ${projected_budget:.2f} (budget) / ${projected_actual:.2f} (actual)")

        if not self.current_user.savings_accounts:
            ctk.CTkLabel(self.savings_container, text="No savings accounts yet.", font=("Arial", 14)).pack(pady=20)
            return

        for i, acct in enumerate(self.current_user.savings_accounts):
            frame = ctk.CTkFrame(self.savings_container, fg_color="#E8F5E9", border_color="#43A047", border_width=2, corner_radius=12)
            frame.pack(padx=10, pady=10, fill="x")

            ctk.CTkLabel(frame, text=f"🏦 {acct.name}", font=("Arial Rounded MT Bold", 16), text_color="black").pack(anchor="w", padx=15, pady=(10, 2))
            ctk.CTkLabel(frame, text=f"💵 ${acct.amount:.2f}", font=("Arial", 13), text_color="gray").pack(anchor="w", padx=15, pady=(0, 10))

            action_frame = ctk.CTkFrame(frame, fg_color="transparent")
            action_frame.pack(anchor="e", padx=10, pady=5)

            ctk.CTkButton(action_frame, text="Edit", width=60, command=lambda idx=i: self.edit_savings(idx)).pack(side="left", padx=5)
            ctk.CTkButton(action_frame, text="Delete", width=60, fg_color="red", command=lambda idx=i: self.delete_savings(idx)).pack(side="left", padx=5)

    def open_add_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add Savings Account")
        popup.geometry("360x300")
        popup.transient(self)
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(popup, text="New Savings Account", font=("Arial Rounded MT Bold", 18)).pack(pady=(15, 5))

        name_entry = ctk.CTkEntry(popup, placeholder_text="Account Name")
        name_entry.pack(pady=5, padx=20, fill="x")

        amount_entry = ctk.CTkEntry(popup, placeholder_text="Amount Saved")
        amount_entry.pack(pady=5, padx=20, fill="x")

        def save():
            try:
                name = name_entry.get()
                amount = float(amount_entry.get())
                if not name:
                    raise ValueError("Name is required")

                new_saving = SavingsAccount(name=name, amount=amount)
                self.current_user.savings_accounts.append(new_saving)
                save_single_user(self.current_user)
                self.render_savings()
                popup.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid name and number.")

        ctk.CTkButton(popup, text="💾 Save", command=save).pack(pady=15)

    def edit_savings(self, index):
        account = self.current_user.savings_accounts[index]

        popup = ctk.CTkToplevel(self)
        popup.title("Edit Savings Account")
        popup.geometry("360x300")
        popup.transient(self)
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(popup, text="Edit Savings", font=("Arial Rounded MT Bold", 18)).pack(pady=(15, 5))

        name_entry = ctk.CTkEntry(popup)
        name_entry.insert(0, account.name)
        name_entry.pack(pady=5, padx=20, fill="x")

        amount_entry = ctk.CTkEntry(popup)
        amount_entry.insert(0, str(account.amount))
        amount_entry.pack(pady=5, padx=20, fill="x")

        def save_changes():
            try:
                account.name = name_entry.get()
                account.amount = float(amount_entry.get())
                save_single_user(self.current_user)
                self.render_savings()
                popup.destroy()
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number.")

        ctk.CTkButton(popup, text="Save Changes", command=save_changes).pack(pady=15)

    def delete_savings(self, index):
        confirm = messagebox.askyesno("Confirm", "Delete this savings account?")
        if confirm:
            self.current_user.savings_accounts.pop(index)
            save_single_user(self.current_user)
            self.render_savings()

    def back_to_dashboard(self):
        self.switch_to("dashboard", user=self.current_user)