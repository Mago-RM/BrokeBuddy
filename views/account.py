'''
    Account Frame allows users to Update their account information
    Change Password
    Change email
    Delete Account

    Frame uses popup windows for interaction
'''
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
from customtkinter import CTkImage

from logic.auth import get_user, delete_user, create_user, save_all_users, load_all_users

#    - - - - - - - - - - - >  A C C O U N T < - - - - - -
class AccountFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to):
        super().__init__(master)
        self.switch_to = switch_to

        # Background
        try:
            bg_image = Image.open("assets/money_bg.jpg").resize((1920, 1080))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Background image not found.")

        # Main container
        self.container = ctk.CTkFrame(self, fg_color="#4CAF50", corner_radius=15)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3, relheight=0.65)

        # Title
        self.title_label = ctk.CTkLabel(
            self.container,
            text="Account Settings",
            font=("Arial Rounded MT Bold", 24),
            text_color="white"
        )
        self.title_label.pack(pady=(30, 10))

        #Logo
        try:
            image = Image.open("assets/cute_doge_circle.png")
            self.photo = CTkImage(dark_image=image, light_image=image, size=(200, 200))
            self.image_label = ctk.CTkLabel(self.container, image=self.photo, text="")
            self.image_label.pack(pady=10)
        except FileNotFoundError:
            print("Image not found. Check image path.")

        # Change Email Button
        self.change_email_button = ctk.CTkButton(
            self.container,
            text="Change Email",
            fg_color="#4CAF50",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=self.change_email_popup
        )
        self.change_email_button.pack(pady=10)

        # Change Password Button
        self.change_password_button = ctk.CTkButton(
            self.container,
            text="Change Password",
            fg_color="#4CAF50",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=self.change_password_popup
        )
        self.change_password_button.pack(pady=10)

        # Delete Button
        self.delete_button = ctk.CTkButton(
            self.container,
            text="Delete Account",
            fg_color="red",
            hover_color="#E53935",
            text_color="white",
            width=240,
            command=self.delete_account
        )
        self.delete_button.pack(pady=10)

        # Back Button
        self.back_button = ctk.CTkButton(
            self.container,
            text="Back",
            fg_color="#4CAF50",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=lambda: (
                #print("Back to dashboard with user:", self.current_user_id), #Debug
                self.switch_to("dashboard", user=self.current_user)
            )
        )
        self.back_button.pack(pady=(10, 20))

    #       - - - - - > A C T I O N S < - - - -
    def set_user(self, user):
        self.current_user = user

    def change_email_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Change Email")
        popup.geometry("300x180")
        popup.grab_set()

        label = ctk.CTkLabel(popup, text="New Email:")
        label.pack(pady=(20, 5))

        email_entry = ctk.CTkEntry(popup, width=200)
        email_entry.pack(pady=5)

        def update_email():
            new_email = email_entry.get().strip()
            if not new_email:
                messagebox.showwarning("Input Error", "Please enter an email.")
                return

            data = load_all_users("data.json")
            if self.current_user.user_id in data["users"]:
                data["users"][self.current_user.user_id]["email"] = new_email
                save_all_users(data, "data.json")
                messagebox.showinfo("Done", "Your email has been updated.")
                popup.destroy()
            else:
                messagebox.showerror("Error", "User not found.")

        update_btn = ctk.CTkButton(popup, text="Update", command=update_email)
        update_btn.pack(pady=(10, 5))

        cancel_btn = ctk.CTkButton(popup, text="Cancel", fg_color="#C2DCC8", hover_color="#AABFB1", command=popup.destroy)
        cancel_btn.pack()

    def change_password_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Change Password")
        popup.geometry("300x300")
        popup.grab_set()

        label1 = ctk.CTkLabel(popup, text="New Password:")
        label1.pack(pady=(20, 5))
        pass_entry = ctk.CTkEntry(popup, show="*", width=200)
        pass_entry.pack(pady=5)

        label2 = ctk.CTkLabel(popup, text="Confirm Password:")
        label2.pack(pady=5)
        confirm_entry = ctk.CTkEntry(popup, show="*", width=200)
        confirm_entry.pack(pady=5)

        def update_password():
            p1 = pass_entry.get()
            p2 = confirm_entry.get()
            if not p1 or not p2:
                messagebox.showwarning("Input Error", "Please fill out both fields.")
                return

            if p1 != p2:
                messagebox.showerror("Mismatch", "Passwords do not match.")
                return

            data = load_all_users("data.json")
            if self.current_user.user_id in data["users"]:
                data["users"][self.current_user.user_id]["password"] = p1
                save_all_users(data, "data.json")
                messagebox.showinfo("Done", "Password has been updated.")
                popup.destroy()
            else:
                messagebox.showerror("Error", "User not found.")

        update_btn = ctk.CTkButton(popup, text="Update", command=update_password)
        update_btn.pack(pady=(10, 5))

        cancel_btn = ctk.CTkButton(popup, text="Cancel", fg_color="#C2DCC8", hover_color="#AABFB1", command=popup.destroy)
        cancel_btn.pack()

    def delete_account(self):
        confirm = messagebox.askyesno("Delete Account", "Are you sure you want to delete your account?")
        if confirm:
            delete_user(self.current_user.user_id)  # Using User passed to frame.
            messagebox.showinfo("Deleted", "Your account has been deleted.")
            self.switch_to("welcome")
