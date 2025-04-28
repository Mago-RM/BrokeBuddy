import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from logic.auth import get_user, create_user, delete_user, load_all_users, save_all_users
from logic.models import User
from views.savings import SavingsFrame
#Import Other Frames
from views.welcomeFrame import WelcomeFrame
from views.LoginSignup import LoginSignUpFrame
from views.SignIn import SignInFrame
from views.SignUp import SignUpFrame
from views.dashboard import dashFrame
from views.account import AccountFrame
from views.cards import CardsFrame
from views.income import IncomeFrame
from views.recurrent import RecurrentFrame
from views.budgetFrame import BudgetFrame
from views.graphs import GraphsFrame
from views.ExpensesFrame import ExpensesFrame

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class BrokeBuddyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BrokeBuddy 🐷💸")
        self.attributes("-fullscreen", True)  # True fullscreen without taskbar
        self.state("zoomed")
        self.configure(fg_color="#4CAF50")

        self.frames = {}
        self.create_frames()
        self.show_frame("welcome")

        # Bind Escape to exit fullscreen mode, F11 to enter fullscreen
        self.bind("<Escape>", self.exit_fullscreen)
        self.bind("<F11>", self.toggle_fullscreen)

    #Aliases for all frames ("Views")
    def create_frames(self):
        self.frames["welcome"] = WelcomeFrame(self, switch_to=self.show_frame)
        self.frames["login"] = LoginSignUpFrame(self, switch_to=self.show_frame)
        self.frames["signin"] = SignInFrame(self, switch_to=self.show_frame)
        self.frames["signup"] = SignUpFrame(self, switch_to=self.show_frame)
        self.frames["dashboard"] = dashFrame(self, switch_to=self.show_frame)
        self.frames["account"] = AccountFrame(self, switch_to=self.show_frame)
        self.frames["cards"] = CardsFrame(self, switch_to=self.show_frame)
        self.frames["income"] = IncomeFrame(self, switch_to=self.show_frame)
        self.frames["savings"] = SavingsFrame(self, switch_to=self.show_frame)
        self.frames["recurrent"] = RecurrentFrame(self, switch_to=self.show_frame)
        self.frames["budgets"] = BudgetFrame(self, switch_to=self.show_frame) #Budget Is calculated based on Whats "left" after recurrent
        self.frames["transactions"] = ExpensesFrame(self, switch_to=self.show_frame) #Expenses are tied to a budget category  or "other/misc/onetime.."
        self.frames["graphs"] = GraphsFrame(self, switch_to=self.show_frame)

    #Passes User to each Frame
    def show_frame(self, name, user=None):
        for frame in self.frames.values():
            frame.pack_forget()

        frame = self.frames[name]

        if user and hasattr(frame, "set_user"):
            frame.set_user(user)

        frame.pack(expand=True, fill="both")
        frame.update_idletasks()
        frame.update()

    def exit_fullscreen(self, event=None):
        """
        Exit fullscreen mode when Escape is pressed.
        """
        self.attributes("-fullscreen", False)

    def toggle_fullscreen(self, event=None):
        """
            Toggle fullscreen mode on and off.
        """
        is_fullscreen = self.attributes("-fullscreen")
        self.attributes("-fullscreen", not is_fullscreen)


#               - - - - - - - > S T A R T   L O O P  < - - - - - -
if __name__ == "__main__":
    app = BrokeBuddyApp()
    app.mainloop()


