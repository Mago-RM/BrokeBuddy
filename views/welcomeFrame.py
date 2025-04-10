#This is the Initial Frame for UI

import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from logic.auth import get_user, create_user, delete_user, load_all_users, save_all_users
from logic.models import User

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# - - - - - - - > S T A R T < - - - - - -
class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to):
        super().__init__(master, fg_color="#4CAF50")
        self.switch_to = switch_to

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.container = ctk.CTkFrame(self, fg_color="#4CAF50")
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=0)
        self.container.rowconfigure(2, weight=0)
        self.container.rowconfigure(3, weight=0)
        self.container.rowconfigure(4, weight=1)

        self.title_label = ctk.CTkLabel(self.container, text="Welcome", font=("Arial", 28, "bold"), text_color="white")
        self.title_label.grid(row=1, column=0, pady=(40, 20))

        try:
            image = Image.open("assets/cute_doge_circle.png")
            self.photo = CTkImage(dark_image=image, light_image=image, size=(200, 200))
            self.image_label = ctk.CTkLabel(self.container, image=self.photo, text="")
            self.image_label.grid(row=2, column=0, pady=10)
        except FileNotFoundError:
            print("Image not found. Check image path.")

        self.start_button = ctk.CTkButton(
            self.container,
            text="Start",
            fg_color="#4CAF50",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=lambda: self.switch_to("login")
        )
        self.start_button.grid(row=3, column=0, pady=20)