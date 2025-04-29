"""Class Allows Users to Reset Credentials """

import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from logic.auth import get_user, create_user, delete_user, load_all_users, save_all_users
from logic.models import User

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class ForgotFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to):
        super().__init__(master)
        self.switch_to = switch_to

        try:
            bg_image = Image.open("assets/money_bg.jpg").resize((1920, 1080))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Background image not found. Check your path.")

        self.container = ctk.CTkFrame(self, fg_color="#4CAF50", corner_radius=15)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.45, relheight=0.65)

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

        self.title_label = ctk.CTkLabel(
            self.inner_container,
            text="Please Enter your Email Address",
            font=("Arial Rounded MT Bold", 24),
            text_color="white"
        )
        self.title_label.pack(pady=(30, 10))


        self.email_entry = ctk.CTkEntry(
            self.inner_container,
            placeholder_text="Email",
            fg_color="white",
            text_color="black",
            border_color="white",
            border_width=1,
            width=240
        )
        self.email_entry.pack(pady=10)


        self.sent_button = ctk.CTkButton(
            self.container,
            text="Submit",
            fg_color="#4CAF50",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=self.forgot_action
        )
        self.sent_button.pack(pady=10)

        self.back_button = ctk.CTkButton(
            self.container,
            text="Back",
            fg_color="#4CAF50",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=self.back_to_login
        )
        self.back_button.pack(pady=10)

    #               - - - - - - - > A C T I O N S  < - - - - - -
    def forgot_action(self):
        email = self.email_entry.get().strip()

        if not email:
            messagebox.showwarning("Missing Email", "Please enter an email address.")
            return

        # Basic email format check
        if "@" not in email or "." not in email:
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        data = load_all_users("data.json")

        # Search for email in user database
        found = False
        for user_info in data.get("users", {}).values():
            if user_info.get("email", "").lower() == email.lower():
                found = True
                break

        if found:
            messagebox.showinfo("Password Reset", "An email with password reset instructions has been sent.")
            self.switch_to("login")
        else:
            messagebox.showerror("Not Found", "No account with that email was found.")
            self.switch_to("login")

    def back_to_login(self):
        print("Going back to login")
        print("Frames available:", self.switch_to.__self__.frames.keys())
        self.switch_to("login")