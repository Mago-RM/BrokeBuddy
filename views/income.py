import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from logic.models import Income
from logic.auth import save_single_user

class IncomeFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to):
        super().__init__(master)
        self.switch_to = switch_to
        self.current_user = None

        self.configure(fg_color="#4CAF50")

        # 📦 Wider main card
        self.container = ctk.CTkFrame(self, fg_color="#4CAF50", corner_radius=15)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.85)

        self.inner_container = ctk.CTkFrame(self.container, fg_color="#4CAF50")
        self.inner_container.pack(expand=True, fill="both", padx=40, pady=30)

        # Title
        self.title = ctk.CTkLabel(self.inner_container, text="💵 Your Income", font=("Arial Rounded MT Bold", 24), text_color="white")
        self.title.pack(pady=(0, 5))

        # Income summary totals
        self.total_label = ctk.CTkLabel(self.inner_container, text="", font=("Arial", 14), text_color="white")
        self.total_label.pack(pady=(0, 10))

        self.income_container = ctk.CTkScrollableFrame(self.inner_container, fg_color="white", corner_radius=10)
        self.income_container.pack(expand=True, fill="both", padx=10, pady=10)

        self.button_frame = ctk.CTkFrame(self.inner_container, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.add_button = ctk.CTkButton(self.button_frame, text="➕ Add Income", command=self.open_add_income_popup)
        self.add_button.pack(side="left", padx=10)

        self.back_button = ctk.CTkButton(self.button_frame, text="⬅ Back", command=self.back_to_dashboard)
        self.back_button.pack(side="left", padx=10)


    def set_user(self, user):
        self.current_user = user
        self.render_income()

    def render_income(self):
        for widget in self.income_container.winfo_children():
            widget.destroy()

        # Show total at top
        est = self.get_estimated_monthly_income()
        self.total_label.configure(text=f"📊 Estimated Monthly Income: ${est:.2f}")

        if not self.current_user.income:
            empty_label = ctk.CTkLabel(self.income_container, text="No income recorded yet.", font=("Arial", 14))
            empty_label.pack(pady=20)
            return

        for i, income in enumerate(self.current_user.income):
            if income.type == "monthly":
                fg = "#E8F5E9";
                border = "#43A047";
                icon = "📅"
            elif income.type == "weekly":
                fg = "#FFFDE7";
                border = "#F9A825";
                icon = "🔁"
            else:
                fg = "#E3F2FD";
                border = "#0288D1";
                icon = "🧾"

            frame = ctk.CTkFrame(self.income_container, fg_color=fg, corner_radius=15, border_color=border,
                                 border_width=2)
            frame.pack(pady=8, padx=10, fill="x")

            ctk.CTkLabel(frame, text=f"{icon} {income.name}", font=("Arial Rounded MT Bold", 16),
                         text_color="black").pack(anchor="w", padx=15, pady=(10, 2))
            ctk.CTkLabel(frame, text=f"💵 ${income.amount:.2f} • {income.type.capitalize()}", font=("Arial", 13),
                         text_color="gray").pack(anchor="w", padx=15)

            # Edit/Delete buttons
            action_frame = ctk.CTkFrame(frame, fg_color="transparent")
            action_frame.pack(anchor="e", padx=10, pady=10)

            ctk.CTkButton(action_frame, text="Edit", width=60, command=lambda idx=i: self.edit_income(idx)).pack(
                side="left", padx=5)
            ctk.CTkButton(action_frame, text="Delete", width=60, fg_color="red",
                          command=lambda idx=i: self.delete_income(idx)).pack(side="left", padx=5)

        self.income_container.update_idletasks()

    def open_add_income_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add Income")
        popup.geometry("360x360")
        popup.transient(self)
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(popup, text="Add New Income", font=("Arial Rounded MT Bold", 18)).pack(pady=(15, 5))

        name_entry = ctk.CTkEntry(popup, placeholder_text="Source (e.g., Job, Scholarship)")
        name_entry.pack(pady=5, padx=20, fill="x")

        amount_entry = ctk.CTkEntry(popup, placeholder_text="Amount (e.g., 500)")
        amount_entry.pack(pady=5, padx=20, fill="x")

        type_var = tk.StringVar(value="one-time")
        type_label = ctk.CTkLabel(popup, text="Type:")
        type_label.pack(pady=(10, 2))
        type_toggle = ctk.CTkSegmentedButton(popup, values=["one-time", "weekly", "monthly"], variable=type_var)
        type_toggle.pack(padx=20, fill="x")

        def save_income():
            name = name_entry.get()
            income_type = type_var.get()
            try:
                amount = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Amount must be a number.")
                return

            if not name:
                messagebox.showerror("Missing Info", "Income source name is required.")
                return

            new_income = Income(name=name, amount=amount, type=income_type, date_added=str(datetime.now().date()))
            self.current_user.income.append(new_income)
            save_single_user(self.current_user)
            self.render_income()
            popup.destroy()

        save_btn = ctk.CTkButton(popup, text="💾 Save", command=save_income)
        save_btn.pack(pady=20)

    def get_estimated_monthly_income(self):
        total = 0
        for income in self.current_user.income:
            if income.type == "monthly":
                total += income.amount
            elif income.type == "weekly":
                total += income.amount * 4
            else:
                total += income.amount
        return total

    def edit_income(self, idx):
        income = self.current_user.income[idx]

        popup = ctk.CTkToplevel(self)
        popup.title("Edit Income")
        popup.geometry("360x360")
        popup.transient(self)  # Keep popup on top
        popup.grab_set()  # Make it modal
        popup.focus_force()
        popup.resizable(False, False)

        ctk.CTkLabel(popup, text="Edit Income", font=("Arial Rounded MT Bold", 18)).pack(pady=(15, 5))

        name_entry = ctk.CTkEntry(popup)
        name_entry.insert(0, income.name)
        name_entry.pack(pady=5, padx=20, fill="x")

        amount_entry = ctk.CTkEntry(popup)
        amount_entry.insert(0, str(income.amount))

    def delete_income(self, idx):
        confirm = messagebox.askyesno("Delete?", "Are you sure you want to delete this income?")
        if confirm:
            self.current_user.income.pop(idx)
            save_single_user(self.current_user)
            self.render_income()

    def back_to_dashboard(self):
        self.switch_to("dashboard", user=self.current_user)
