"""Handles Recurrent Expenses for User"""

import re
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from logic.auth import save_single_user
from logic.budget import convert_due_date_input

#Sets View
class RecurrentFrame(ctk.CTkFrame):
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

        label_container = ctk.CTkFrame(logo_and_labels, fg_color="#4CAF50")
        label_container.pack(side="left", anchor="center")

        self.title = ctk.CTkLabel(label_container, text="🔁 Recurrent Charges", font=("Arial Rounded MT Bold", 24),
                                  text_color="white")
        self.title.pack(anchor="w")

        self.summary_label = ctk.CTkLabel(label_container, text="", font=("Arial", 14), text_color="white")
        self.summary_label.pack(anchor="w")

        self.inner_container = ctk.CTkFrame(self.container, fg_color="#4CAF50")
        self.inner_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)

        self.recurrent_container = ctk.CTkScrollableFrame(self.inner_container, fg_color="white", corner_radius=10)
        self.inner_container.grid_rowconfigure(0, weight=1)

        self.inner_container.grid_columnconfigure(0, weight=1)
        self.inner_container.grid_rowconfigure(0, weight=1)
        self.recurrent_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=(10, 0))

        self.button_frame = ctk.CTkFrame(self.inner_container, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, pady=10)

        self.add_button = ctk.CTkButton(self.button_frame, text="➕ Add Recurrent",
                                        command=self.open_add_recurrent_popup)
        self.add_button.pack(side="left", padx=10)

        self.back_button = ctk.CTkButton(self.button_frame, text="⬅ Back", command=self.back_to_dashboard)
        self.back_button.pack(side="left", padx=10)

    def set_user(self, user):
        """Get User"""
        self.current_user = user
        self.render_recurrents()

    def render_recurrents(self):
        """Gets Recurrent Expenses"""
        for widget in self.recurrent_container.winfo_children():
            widget.destroy()

        total_monthly = 0
        for exp in self.current_user.recurring_expenses:
            if exp.frequency == "weekly":
                total_monthly += exp.amount * 4
            elif exp.frequency == "bi-weekly":
                total_monthly += exp.amount * 2
            else:
                total_monthly += exp.amount

        self.summary_label.configure(text=f"Estimated Monthly Total: ${total_monthly:.2f}")

        if not self.current_user.recurring_expenses:
            ctk.CTkLabel(self.recurrent_container, text="No recurrent expenses added yet.", font=("Arial", 14)).pack(pady=20)
            return

        for idx, exp in enumerate(self.current_user.recurring_expenses):
            frame = ctk.CTkFrame(self.recurrent_container, fg_color="#E8F5E9", border_color="#43A047", border_width=2, corner_radius=12)
            frame.pack(padx=10, pady=10, fill="x")

            label = f"📌 {exp.name}"
            if getattr(exp, "is_membership", False):
                label += " (Membership)"

            ctk.CTkLabel(frame, text=label, font=("Arial Rounded MT Bold", 16), text_color="black").pack(anchor="w", padx=15, pady=(10, 2))
            ctk.CTkLabel(frame, text=f"💰 ${exp.amount:.2f} - {exp.frequency.capitalize()}", font=("Arial", 13), text_color="gray").pack(anchor="w", padx=15)
            if exp.due_date:
                ctk.CTkLabel(frame, text=f"📅 Due: {exp.due_date}", font=("Arial", 12), text_color="#BF360C").pack(anchor="w", padx=15)

            action_frame = ctk.CTkFrame(frame, fg_color="transparent")
            action_frame.pack(anchor="e", padx=10, pady=10)

            ctk.CTkButton(action_frame, text="Edit", width=60, command=lambda i=idx: self.edit_recurrent(i)).pack(side="left", padx=5)
            ctk.CTkButton(action_frame, text="Delete", width=60, fg_color="red", command=lambda i=idx: self.delete_recurrent(i)).pack(side="left", padx=5)

    def open_add_recurrent_popup(self):
        """Adds a new Recurrent Expense. Opens a popup window."""
        popup = ctk.CTkToplevel(self)
        popup.title("Add Recurrent Charge")
        popup.geometry("360x460")
        popup.transient(self)
        popup.grab_set()

        ctk.CTkLabel(popup, text="Add Recurrent Charge", font=("Arial Rounded MT Bold", 18)).pack(pady=(15, 5))

        name_entry = ctk.CTkEntry(popup, placeholder_text="Expense Name")
        name_entry.pack(pady=5, padx=20, fill="x")

        amount_entry = ctk.CTkEntry(popup, placeholder_text="Amount")
        amount_entry.pack(pady=5, padx=20, fill="x")

        type_var = tk.StringVar(value="monthly")
        toggle = ctk.CTkSegmentedButton(popup, values=["weekly", "bi-weekly", "monthly"], variable=type_var)
        toggle.pack(padx=20, pady=5)

        due_date_entry = ctk.CTkEntry(popup, placeholder_text="First Due Date (MM/DD)")
        due_date_entry.pack(pady=5, padx=20, fill="x")

        membership_var = tk.BooleanVar()
        membership_check = ctk.CTkCheckBox(popup, text="Membership?", variable=membership_var)
        membership_check.pack(pady=(10, 5))

        def save():
            try:
                name = name_entry.get()
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive")

                recurring_type = type_var.get()
                due_raw = due_date_entry.get().strip()

                # Validate MM/DD format
                if not re.match(r"^(0[1-9]|1[0-2])/([0-2][0-9]|3[01])$", due_raw):
                    messagebox.showerror("Invalid Date", "Enter due date in MM/DD format (e.g., 04/15)")
                    return

                due_date = convert_due_date_input(due_raw)
                is_member = membership_var.get()

                # Ensure Recurrent category exists
                if "Recurrent" not in self.current_user.budget_categories:
                    cat_popup = ctk.CTkToplevel(self)
                    cat_popup.title("Create 'Recurrent' Category")
                    cat_popup.geometry("300x200")
                    cat_popup.transient(self)
                    cat_popup.grab_set()

                    ctk.CTkLabel(cat_popup, text="Monthly limit for 'Recurrent' category:").pack(pady=10)
                    limit_entry = ctk.CTkEntry(cat_popup, placeholder_text="e.g., 200")
                    limit_entry.pack(pady=5, padx=20)

                    def create_category():
                        try:
                            limit = float(limit_entry.get())
                            from logic.models import BudgetCategory
                            self.current_user.budget_categories["Recurrent"] = BudgetCategory("Recurrent", limit)
                            save_single_user(self.current_user)
                            cat_popup.destroy()
                        except ValueError:
                            messagebox.showerror("Invalid Input", "Limit must be a number.")

                    ctk.CTkButton(cat_popup, text="✅ Create", command=create_category).pack(pady=10)
                    return

                # Convert to monthly cost
                monthly_amount = amount
                if recurring_type == "weekly":
                    monthly_amount *= 4
                elif recurring_type == "bi-weekly":
                    monthly_amount *= 2

                from logic.models import Expense
                new_expense = Expense(
                    name=name,
                    amount=amount,
                    category="Recurrent",
                    recurring=True,
                    frequency=recurring_type,
                    due_date=due_date,
                    is_membership=is_member
                )

                self.current_user.recurring_expenses.append(new_expense)
                self.current_user.budget_categories["Recurrent"].add_expense(monthly_amount)

                save_single_user(self.current_user)
                self.render_recurrents()
                popup.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(popup, text="💾 Save", command=save).pack(pady=15)

    def edit_recurrent(self, index):
        """Allows user to edit a posted Recurrent Expense """
        exp = self.current_user.recurring_expenses[index]
        old_amount = exp.amount
        old_type = exp.frequency

        popup = ctk.CTkToplevel(self)
        popup.title("Edit Recurrent")
        popup.geometry("360x420")
        popup.transient(self)
        popup.grab_set()

        name_entry = ctk.CTkEntry(popup)
        name_entry.insert(0, exp.name)
        name_entry.pack(pady=5, padx=20, fill="x")

        amount_entry = ctk.CTkEntry(popup)
        amount_entry.insert(0, str(exp.amount))
        amount_entry.pack(pady=5, padx=20, fill="x")

        type_var = tk.StringVar(value=exp.frequency)
        toggle = ctk.CTkSegmentedButton(popup, values=["weekly", "bi-weekly", "monthly"], variable=type_var)
        toggle.pack(padx=20, pady=5)

        due_date_entry = ctk.CTkEntry(popup)
        due_date_entry.insert(0, exp.due_date)
        due_date_entry.pack(pady=5, padx=20, fill="x")

        membership_var = tk.BooleanVar(value=getattr(exp, "is_membership", False))
        membership_check = ctk.CTkCheckBox(popup, text="Membership?", variable=membership_var)
        membership_check.pack(pady=(10, 5))

        def save_changes():
            try:
                new_amount = float(amount_entry.get())
                new_type = type_var.get()

                if new_amount <= 0:
                    raise ValueError("Amount must be a positive number.")

                # Monthly equivalents
                old_monthly = old_amount
                if old_type == "weekly":
                    old_monthly *= 4
                elif old_type == "bi-weekly":
                    old_monthly *= 2

                new_monthly = new_amount
                if new_type == "weekly":
                    new_monthly *= 4
                elif new_type == "bi-weekly":
                    new_monthly *= 2

                # Update category budget
                category = self.current_user.budget_categories.get("Recurrent")
                if category:
                    category.spent -= old_monthly
                    category.spent += new_monthly
                    category.spent = max(0, category.spent)

                # Update the expense
                exp.name = name_entry.get()
                exp.amount = new_amount
                exp.frequency = new_type
                exp.due_date = due_date_entry.get()
                exp.is_membership = membership_var.get()

                save_single_user(self.current_user)
                self.render_recurrents()
                popup.destroy()

            except ValueError:
                messagebox.showerror("Error", "Invalid input")

        ctk.CTkButton(popup, text="💾 Save Changes", command=save_changes).pack(pady=15)

    def delete_recurrent(self, index):
        """Allows User to Delete a Recurrent Expense """
        confirm = messagebox.askyesno("Confirm", "Delete this recurrent charge?")
        if confirm:
            expense = self.current_user.recurring_expenses[index]

            monthly_cost = expense.amount
            if expense.frequency == "weekly":
                monthly_cost *= 4
            elif expense.frequency == "bi-weekly":
                monthly_cost *= 2

            category = self.current_user.budget_categories.get("Recurrent")
            if category:
                category.spent -= monthly_cost
                category.spent = max(0, category.spent)

            self.current_user.recurring_expenses.pop(index)
            save_single_user(self.current_user)
            self.render_recurrents()

    def back_to_dashboard(self):
        """Switches back to Dashboard"""
        self.switch_to("dashboard", user=self.current_user)
