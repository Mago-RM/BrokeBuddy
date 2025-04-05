import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from logic.auth import get_user, create_user, delete_user, load_all_users, save_all_users
from logic.models import User

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class BrokeBuddyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BrokeBuddy 🐷💸")
        self.state("zoomed")  # Fullscreen on startup
        self.configure(fg_color="#4CAF50")

        self.frames = {}
        self.create_frames()
        self.show_frame("welcome")

    #Aliases for all frames ("Views")
    def create_frames(self):
        self.frames["welcome"] = WelcomeFrame(self, switch_to=self.show_frame)
        self.frames["login"] = LoginSignUpFrame(self, switch_to=self.show_frame)
        self.frames["signin"] = SignInFrame(self, switch_to=self.show_frame)
        self.frames["signup"] = SignUpFrame(self, switch_to=self.show_frame)
        self.frames["dashboard"] = dashFrame(self, switch_to=self.show_frame)

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget() #Hides Frames
        self.frames[name].pack(expand=True, fill="both") #Show only selected one

# - - - - - - - > S T A R T < - - - - - -
class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to):
        super().__init__(master, fg_color="#4CAF50")
        self.switch_to = switch_to

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.container = ctk.CTkFrame(self, fg_color="#4CAF50")
        self.container.grid(row=0, column=0, sticky="nsew", padx=60, pady=60)

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

#               - - - - - - - > W E L C O M E  < - - - - - -
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
        self.back_button.pack(pady=10)

    def signin_action(self):
        self.switch_to("signin")

    def signup_action(self):
        self.switch_to("signup")


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
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Missing Info", "Please enter both username and password.")
            return

        user = get_user(username, password)

        if not username or not password:
            messagebox.showwarning("Missing Info", "Please enter both username and password.")
            return

        user = get_user(username, password)

        if user:
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.switch_to("dashboard")  # or whatever screen will show at login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")


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


#               - - - - - - - > D A S H B O A R D  < - - - - - -
class dashFrame(ctk.CTkFrame):
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

        # Title
        self.title_label = ctk.CTkLabel(
            self.inner_container,
            text="Dashboard Overview",
            font=("Arial Rounded MT Bold", 24),
            text_color="white"
        )
        self.title_label.pack(pady=10)

        # Spending chart placeholder
        self.spending_chart = ctk.CTkLabel(
            self.inner_container,
            text="[Spending Chart Placeholder]",
            width=240,
            height=120,
            fg_color="white",
            text_color="black",
            corner_radius=10
        )
        self.spending_chart.pack(pady=10)

        # Savings progress
        self.savings_progress = ctk.CTkLabel(
            self.inner_container,
            text="[Savings Progress Placeholder]",
            width=240,
            height=60,
            fg_color="white",
            text_color="black",
            corner_radius=10
        )
        self.savings_progress.pack(pady=10)

        # Navigation buttons
        self.nav_bar = ctk.CTkFrame(self, fg_color="#388E3C", corner_radius=0)
        self.nav_bar.pack(side="bottom", fill="x")

        for label in ["Income", "Budgets", "Expenses", "Recurring", "Graphs"]:
            btn = ctk.CTkButton(self.nav_bar, text=label, fg_color="white", text_color="#388E3C")
            btn.pack(side="left", expand=True, fill="x", padx=2, pady=2)

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
    # Graphs, Budgets, Expenses, Recurrent Charges, Income,
    def back_to_login(self):
        self.switch_to("login")


#               - - - - - - - > S T A R T   L O O P  < - - - - - -
if __name__ == "__main__":
    app = BrokeBuddyApp()
    app.mainloop()

#Forgot password
#Dashboard PlaceHolder
#connect create account
#Budget Screen
#Expenses List
#More Screens