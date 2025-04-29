"""     Second Frame for user to Log In or Sign Up      """

import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from logic.auth import get_user, create_user, delete_user, load_all_users, save_all_users
from logic.models import User

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

#               - - - - - - - > Login/SignUp  < - - - - - -
class LoginSignUpFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to):
        super().__init__(master)
        self.switch_to = switch_to

        try:
            #Load Background
            bg_image = Image.open("assets/money_bg.jpg").resize((1920, 1080))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Background image not found. Check image path.")

        self.container = ctk.CTkFrame(self, fg_color="#4CAF50", corner_radius=15)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.25, relheight=0.6)

        self.inner_container = ctk.CTkFrame(self.container, fg_color="#4CAF50")
        self.inner_container.pack(expand=True, fill="both", padx=40, pady=30)

        try:
            #Load Logo
            image = Image.open("assets/cute_doge_circle.png")
            self.photo = CTkImage(dark_image=image, light_image=image, size=(100, 100))
            self.image_label = ctk.CTkLabel(self.inner_container, image=self.photo, text="")
            self.image_label.pack(pady=10)
        except FileNotFoundError:
            print("Image not found. Check image path.")

        self.title_label = ctk.CTkLabel(
            self.inner_container,
            text="Welcome",
            font=("Arial Rounded MT Bold", 24),
            text_color="white"
        )
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.inner_container,
            text="Great to see you here!",
            font=("Arial", 14),
            text_color="white"
        )
        self.subtitle_label.pack(pady=5)

        #Login Button
        self.login_button = ctk.CTkButton(
            self.inner_container,
            text="Sign In",
            fg_color="#4CAF50",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=self.signin_action
        )
        self.login_button.pack(pady=10)

        #SignUp Button
        self.signup_button = ctk.CTkButton(
            self.inner_container,
            text="Sign Up",
            fg_color="#4CAF50",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=self.signup_action
        )
        self.signup_button.pack(pady=10)

        # Forgot Pass Button
        self.forgot_button = ctk.CTkButton(
            self.inner_container,
            text="Forgot Password?",
            fg_color="#4CAF50",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=self.forgot_action
        )
        self.forgot_button.pack(pady=10)

        #Back Button
        self.back_button = ctk.CTkButton(
            self.inner_container,
            text="Back",
            fg_color="#4CAF50",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=lambda: self.switch_to("welcome")
        )
        self.back_button.pack(pady=20)

    def signin_action(self):
        self.switch_to("signin")

    def signup_action(self):
        self.switch_to("signup")

    def forgot_action(self):
        self.switch_to("forgot")