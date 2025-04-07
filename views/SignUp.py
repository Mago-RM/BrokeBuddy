import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from logic.auth import get_user, create_user, delete_user, load_all_users, save_all_users
from logic.models import User

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

#               - - - - - - - > S I G N   U P   < - - - - - -
class SignUpFrame(ctk.CTkFrame):
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
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.25, relheight=0.85)

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
            text="Sign Up",
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

        self.password_entry = ctk.CTkEntry(self.inner_container, fg_color="white", placeholder_text="Password", show="*", width=240)
        self.password_entry.pack(pady=10)

        self.password2_entry = ctk.CTkEntry(self.inner_container, fg_color="white", placeholder_text="Confirm Password", show="*", width=240)
        self.password2_entry.pack(pady=10)

        self.signup_button = ctk.CTkButton(
            self.container,
            text="Sign Up",
            fg_color="#4CAF50",
            border_color="white",
            border_width=2,
            text_color="white",
            hover_color="#43a047",
            command=self.signup_action
        )
        self.signup_button.pack(pady=10)

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
    def signup_action(self):
        username = self.username_entry.get().strip()
        # TODO: Add format validation for email
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.password2_entry.get().strip()

        if not username or not email or not password or not confirm:
            messagebox.showwarning("Incomplete Form", "Please fill in all fields.")
        elif password != confirm:
            messagebox.showerror("Password Mismatch", "Passwords do not match.")
        else:
            data = load_all_users("data.json")

            if username in data["users"]:
                messagebox.showerror("User Exists", f"A user with username '{username}' already exists.")
                return

            user = User(username)
            user_data = user.to_dict()
            user_data["password"] = password
            user_data["email"] = email

            data["users"][username] = user_data
            save_all_users(data, "data.json")

            messagebox.showinfo("Success", f"Account created for {username}!")
            self.switch_to("signin")

    def back_to_login(self):
        print("Going back to login")
        print("Frames available:", self.switch_to.__self__.frames.keys())
        self.switch_to("login")