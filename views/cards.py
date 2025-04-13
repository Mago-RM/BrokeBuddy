import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from logic.models import Card
from logic.auth import save_all_users, load_all_users, save_single_user


class CardsFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to):
        super().__init__(master)
        self.switch_to = switch_to
        self.current_user = None

        # Frame background color
        self.configure(fg_color="#4CAF50")  # BrokeBuddy green

        # Title
        self.title = ctk.CTkLabel(
            self,
            text="💳 Your Cards",
            font=("Arial Rounded MT Bold", 24),
            text_color="white"
        )
        self.title.pack(pady=10)

        # Card container (scrollable)
        self.cards_container = ctk.CTkScrollableFrame(self, fg_color="#66BB6A")  # lighter green for contrast
        self.cards_container.pack(expand=True, fill="both", pady=10, padx=20)

        # Button Frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        # Styled Buttons
        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="➕ Add Card",
            fg_color="#43A047",  # darker green
            hover_color="#388E3C",
            text_color="white",
            corner_radius=10,
            command=self.open_add_card_popup
        )
        self.add_button.pack(side="left", padx=10)

        self.back_button = ctk.CTkButton(
            self.button_frame,
            text="⬅ Back",
            fg_color="white",
            hover_color="#EEEEEE",
            text_color="#4CAF50",
            border_color="#4CAF50",
            border_width=2,
            corner_radius=10,
            command=self.back_to_dashboard
        )
        self.back_button.pack(side="left", padx=10)


    # -    -   -   -   -   - ACTIONS -  -   -   -
    def set_user(self, user):
        self.current_user = user
        self.render_cards()

    def render_cards(self):
        for widget in self.cards_container.winfo_children():
            widget.destroy()

        if not self.current_user.cards:
            empty_label = ctk.CTkLabel(self.cards_container, text="No cards saved yet. Add one below!", font=("Arial", 14))
            empty_label.pack(pady=20)
            return

        # Calculate totals
        total_debit = sum(c.balance for c in self.current_user.cards if c.type == "debit")
        total_credit = sum(c.balance for c in self.current_user.cards if c.type == "credit")

        summary_frame = ctk.CTkFrame(self.cards_container, fg_color="transparent")
        summary_frame.pack(pady=(0, 5), padx=10, fill="x")

        ctk.CTkLabel(
            summary_frame,
            text=f"💰 Debit Total: ${total_debit:.2f}",
            text_color="#2E7D32",  # green
            font=("Arial Rounded MT Bold", 14)
        ).pack(side="left", padx=5)

        ctk.CTkLabel(
            summary_frame,
            text=f"💳 Credit Total: ${total_credit:.2f}",
            text_color="#C62828",  # red
            font=("Arial Rounded MT Bold", 14)
        ).pack(side="right", padx=5)

        for idx, card in enumerate(self.current_user.cards):
            card_color = "#E8F5E9" if card.type == "debit" else "#FFEBEE"  # light green vs. light red
            border_color = "#43A047" if card.type == "debit" else "#C62828"  # green vs. red

            card_frame = ctk.CTkFrame(
                self.cards_container,
                fg_color=card_color,
                corner_radius=15,
                border_color=border_color,
                border_width=2
            )

            name_label = ctk.CTkLabel(card_frame, text=f"🏦 {card.name}", text_color="black", font=("Arial Rounded MT Bold", 16))
            name_label.pack(anchor="w", padx=15, pady=(10, 2))

            balance_label = ctk.CTkLabel(card_frame, text=f"💰 ${card.balance:.2f}", text_color="black", font=("Arial", 14))
            balance_label.pack(anchor="w", padx=15)

            # Type (debit/credit)
            card_type = "Credit Card 💳" if card.type == "credit" else "Debit Card 🏦"
            label_type = ctk.CTkLabel(card_frame, text=card_type, font=("Arial", 12), text_color="gray")
            label_type.pack(anchor="w", padx=15)

            # Due date (for credit cards)
            if card.type == "credit" and card.due_date:
                due_label = ctk.CTkLabel(card_frame, text=f"Due: {card.due_date}", font=("Arial", 12),
                                         text_color="#B71C1C")
                due_label.pack(anchor="w", padx=15)

            action_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            action_frame.pack(anchor="e", padx=10, pady=10)

            edit_btn = ctk.CTkButton(action_frame, text="Edit", width=60, command=lambda i=idx: self.edit_card(i))
            edit_btn.pack(side="left", padx=5)

            del_btn = ctk.CTkButton(action_frame, text="Delete", width=60, fg_color="red", command=lambda i=idx: self.delete_card(i))
            del_btn.pack(side="left", padx=5)

            card_frame.pack(pady=10, padx=10, fill="x")

    def open_add_card_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add New Card")
        popup.geometry("360x420")
        popup.transient(self)
        popup.grab_set()
        popup.focus_force()
        popup.resizable(False, False)
        popup.configure(fg_color="#E8F5E9")

        ctk.CTkLabel(popup, text="Add Card", font=("Arial Rounded MT Bold", 20)).pack(pady=(15, 10))

        name_entry = ctk.CTkEntry(popup, placeholder_text="Card Name")
        name_entry.pack(pady=5, padx=20, fill="x")

        balance_entry = ctk.CTkEntry(popup, placeholder_text="Balance (e.g., 500)")
        balance_entry.pack(pady=5, padx=20, fill="x")

        type_frame = ctk.CTkFrame(popup, fg_color="transparent")
        type_frame.pack(pady=5)

        card_type_var = tk.StringVar(value="debit")

        ctk.CTkLabel(type_frame, text="Card Type:").pack(anchor="w", padx=10)

        toggle = ctk.CTkSegmentedButton(type_frame, values=["debit", "credit"], variable=card_type_var)
        toggle.pack(padx=10, pady=2)

        # Due Day (for credit cards only)
        due_entry = ctk.CTkEntry(popup, placeholder_text="Due Day (1–31)")
        due_entry.pack(pady=5, padx=20, fill="x")

        def update_due_entry(*args):
            if card_type_var.get() == "credit":
                due_entry.configure(state="normal")
            else:
                due_entry.delete(0, "end")
                due_entry.configure(state="disabled")

        card_type_var.trace_add("write", update_due_entry)
        update_due_entry()

        def save_card():
            name = name_entry.get()
            card_type = card_type_var.get()
            due_date = due_entry.get().strip() if card_type == "credit" else ""

            try:
                balance = float(balance_entry.get())
                if card_type == "credit" and balance > 0:
                    balance = -abs(balance)
            except ValueError:
                messagebox.showerror("Invalid Input", "Balance must be a number.")
                return

            if not name:
                messagebox.showerror("Missing Name", "Card name is required.")
                return

            if card_type == "credit":
                try:
                    due_day = int(due_date)
                    if not (1 <= due_day <= 31):
                        raise ValueError
                    due_date = str(due_day)
                except ValueError:
                    messagebox.showerror("Invalid Due Day", "Enter a day between 1 and 31.")
                    return

            new_card = Card(name=name, balance=balance, type=card_type, due_date=due_date)
            self.current_user.cards.append(new_card)

            from logic.auth import save_single_user
            save_single_user(self.current_user)

            self.render_cards()
            popup.destroy()

        save_btn = ctk.CTkButton(
            popup,
            text="💾 Save Card",
            fg_color="#4CAF50",
            text_color="white",
            hover_color="#388E3C",
            command=save_card
        )
        save_btn.pack(pady=15)

    def edit_card(self, index):
        card = self.current_user.cards[index]
        popup = ctk.CTkToplevel(self)
        popup.title("Edit Card")
        popup.geometry("300x200")

        name_entry = ctk.CTkEntry(popup)
        name_entry.insert(0, card.name)
        name_entry.pack(pady=10)

        balance_entry = ctk.CTkEntry(popup)
        balance_entry.insert(0, str(card.balance))
        balance_entry.pack(pady=10)

        def save_changes():
            try:
                new_name = name_entry.get()
                new_balance = float(balance_entry.get())
                card.name = new_name
                card.balance = new_balance

                save_single_user(self.current_user)

                self.render_cards()
                popup.destroy()
            except ValueError:
                messagebox.showerror("Error", "Balance must be a number.")

        save_button = ctk.CTkButton(popup, text="Save Changes", command=save_changes)
        save_button.pack(pady=10)

    def delete_card(self, index):
        confirm = messagebox.askyesno("Confirm", "Delete this card?")
        if confirm:
            self.current_user.cards.pop(index)

            save_single_user(self.current_user)

            self.render_cards()

    def back_to_dashboard(self):
        self.switch_to("dashboard", user=self.current_user)
