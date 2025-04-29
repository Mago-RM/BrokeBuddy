import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from logic.auth import get_user
from datetime import datetime
from logic.resetter import MonthResetter


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

#               - - - - - - - > S I G N   I N  < - - - - - -
class SignInFrame(ctk.CTkFrame):
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
            text="Sign In",
            font=("Arial Rounded MT Bold", 24),
            text_color="white"
        )
        self.title_label.pack(pady=(30, 10))

        self.username_entry = ctk.CTkEntry(
            self.inner_container,
            placeholder_text="Username",
            fg_color="white",
            text_color="black",
            border_color="white",
            border_width=1,
            width=240
        )
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self.inner_container,
            placeholder_text="Password",
            show="*",
            fg_color="white",
            text_color="black",
            border_color="white",
            border_width=1,
            width=240
        )
        self.password_entry.pack(pady=10)

        self.signin_button = ctk.CTkButton(
            self.container,
            text="Sign In",
            fg_color="#4CAF50",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=self.signin_action
        )
        self.signin_button.pack(pady=10)

        self.back_button = ctk.CTkButton(
            self.container,
            text="Back",
            fg_color="#4CAF50",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=lambda: self.switch_to("welcome")
        )
        self.back_button.pack(pady=10)

    #               - - - - - - - > A C T I O N S  < - - - - - -

    def signin_action(self):
        """Handles LogIn Credentials and also checks for Reset"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Missing Info", "Please enter both username and password.")
            return

        user = get_user(username, password)

        if user:
            current_month = datetime.now().month

            if hasattr(user, "last_saved_month"):
                if user.last_saved_month != current_month:
                    # If Month is different --> needs resetting! Asks user to do so!
                    answer = messagebox.askyesno(
                        "New Month!",
                        "It's a new month! Would you like to update your savings now?"
                    )

                    if answer:
                        self.switch_to("savings", user=user)
                        return
                    else:
                        # If user says NO, load dashboard
                        self.switch_to("dashboard", user=user)
                        return
                else:
                    # Month matches, normal login
                    self.switch_to("dashboard", user=user)
            else:
                self.switch_to("dashboard", user=user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")