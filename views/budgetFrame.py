import customtkinter as ctk
import tkinter.messagebox as messagebox
from logic.models import BudgetCategory
from logic.auth import save_single_user

class BudgetFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to):
        super().__init__(master)
        self.switch_to = switch_to
        self.current_user = None

        self.configure(fg_color="#4CAF50")

        self.title = ctk.CTkLabel(self, text="🧲 Your Budgets", font=("Arial Rounded MT Bold", 24), text_color="white")
        self.title.pack(pady=10)

        self.category_container = ctk.CTkScrollableFrame(self, fg_color="white", corner_radius=10)
        self.category_container.pack(expand=True, fill="both", padx=20, pady=10)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.add_button = ctk.CTkButton(self.button_frame, text="➕ Add Category", command=self.open_add_popup)
        self.add_button.pack(side="left", padx=10)

        self.back_button = ctk.CTkButton(self.button_frame, text="⬅ Back", command=self.back_to_dashboard)
        self.back_button.pack(side="left", padx=10)

    def set_user(self, user):
        self.current_user = user
        self.render_categories()

    def render_categories(self):
        for widget in self.category_container.winfo_children():
            widget.destroy()

        if not self.current_user.budget_categories:
            ctk.CTkLabel(self.category_container, text="No budget categories set.", font=("Arial", 14)).pack(pady=20)
            return

        for i, (name, cat) in enumerate(self.current_user.budget_categories.items()):
            percent_used = cat.spent / cat.monthly_limit if cat.monthly_limit else 0
            color = "#E8F5E9" if percent_used <= 1 else "#FFEBEE"
            border = "#43A047" if percent_used <= 1 else "#C62828"

            frame = ctk.CTkFrame(self.category_container, fg_color=color, border_color=border, border_width=2, corner_radius=12)
            frame.pack(padx=10, pady=10, fill="x")

            ctk.CTkLabel(frame, text=f"📋 {name}", font=("Arial Rounded MT Bold", 16), text_color="black").pack(anchor="w", padx=15, pady=(10, 2))
            ctk.CTkLabel(frame, text=f"💸 ${cat.spent:.2f} / ${cat.monthly_limit:.2f}", font=("Arial", 13), text_color="gray").pack(anchor="w", padx=15)

            if name == "Recurrent":
                warning = ctk.CTkLabel(
                    frame,
                    text="⚠️ Deleting this will remove all recurring expenses!",
                    font=("Arial", 11),
                    text_color="red"
                )
                warning.pack(anchor="w", padx=15, pady=(4, 0))

            action_frame = ctk.CTkFrame(frame, fg_color="transparent")
            action_frame.pack(anchor="e", padx=10, pady=10)

            ctk.CTkButton(action_frame, text="Edit", width=60, command=lambda idx=i: self.edit_category(idx)).pack(side="left", padx=5)
            ctk.CTkButton(action_frame, text="Delete", width=60, fg_color="red", command=lambda idx=i: self.delete_category(idx)).pack(side="left", padx=5)

    def open_add_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add Budget Category")
        popup.geometry("360x300")
        popup.transient(self)
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(popup, text="New Budget Category", font=("Arial Rounded MT Bold", 18)).pack(pady=(15, 5))
        name_entry = ctk.CTkEntry(popup, placeholder_text="Category Name")
        name_entry.pack(pady=5, padx=20, fill="x")

        limit_entry = ctk.CTkEntry(popup, placeholder_text="Monthly Limit")
        limit_entry.pack(pady=5, padx=20, fill="x")

        def save():
            name = name_entry.get().strip()
            try:
                limit = float(limit_entry.get())
                if limit < 0:
                    raise ValueError("Negative limit")
                if not name:
                    raise ValueError("Missing name")
                if name in self.current_user.budget_categories:
                    raise ValueError("Category already exists")
                new_cat = BudgetCategory(name, limit)
                self.current_user.budget_categories[name] = new_cat
                save_single_user(self.current_user)
                self.render_categories()
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(popup, text="📅 Save", command=save).pack(pady=15)

    def edit_category(self, index):
        name = list(self.current_user.budget_categories.keys())[index]
        cat = self.current_user.budget_categories[name]

        popup = ctk.CTkToplevel(self)
        popup.title("Edit Budget Category")
        popup.geometry("360x300")
        popup.transient(self)
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(popup, text=f"Edit {name}", font=("Arial Rounded MT Bold", 18)).pack(pady=(15, 5))
        limit_entry = ctk.CTkEntry(popup)
        limit_entry.insert(0, str(cat.monthly_limit))
        limit_entry.pack(pady=5, padx=20, fill="x")

        def save_changes():
            try:
                cat.monthly_limit = float(limit_entry.get())
                if cat.monthly_limit < 0:
                    raise ValueError("Negative limit")
                save_single_user(self.current_user)
                self.render_categories()
                popup.destroy()
            except ValueError:
                messagebox.showerror("Error", "Monthly limit must be a number")

        ctk.CTkButton(popup, text="Save Changes", command=save_changes).pack(pady=15)

    def delete_category(self, index):
        name = list(self.current_user.budget_categories.keys())[index]
        confirm = messagebox.askyesno("Confirm", f"Delete category '{name}'?")
        if confirm:
            if name == "Recurrent":
                # Delete all recurring expenses
                self.current_user.recurring_expenses.clear()
                messagebox.showinfo("Deleted", "All recurring expenses have also been deleted.")

            del self.current_user.budget_categories[name]
            save_single_user(self.current_user)
            self.render_categories()

    def back_to_dashboard(self):
        self.switch_to("dashboard", user=self.current_user)
