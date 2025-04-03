#Initial UI

import customtkinter as ctk
from PIL import Image, ImageTk
from customtkinter import CTkImage

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class WelcomeScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BrokeBuddy 🐷💸")
        self.geometry("400x500")
        self.configure(fg_color="green")

        # --- Welcome label ---
        self.label = ctk.CTkLabel(self, text="Welcome", font=("Arial", 28, "bold"))
        self.label.pack(pady=20)

        # --- Dog image ---
        image = Image.open("assets/cute_doge_circle.png")
        image = image.resize((200, 200))  # Optional for pre-szi

        # Wrap as a CTkImage.mOtherwise theres an error
        self.photo = CTkImage(dark_image=image, light_image=image, size=(200, 200))


        self.image_label = ctk.CTkLabel(self, image=self.photo, text="")
        self.image_label.pack(pady=10)

        # --- Start button ---
        self.start_button = ctk.CTkButton(self, text="Start", command=self.start_app)
        self.start_button.pack(pady=20)

    def start_app(self):
        print("Starting login/signup...")
        self.destroy()
        LoginSignUpScreen()

# Placeholder for next screen
class LoginSignUpScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Log In or Sign Up")
        self.geometry("400x500")
        label = ctk.CTkLabel(self, text="Login/sign-up screen 👤")
        label.pack(pady=30)
        self.mainloop()

if __name__ == "__main__":
    app = WelcomeScreen()
    app.mainloop()
