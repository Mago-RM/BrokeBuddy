#BrokeBuddy

**Group Members:**  
- Margarita Rincon Matamoros  
- Tien Pham

---

##Project Description

**BrokeBuddy** is a Python-based desktop budgeting application designed to help users track and manage their personal finances. The app provides a simple interface for adding income, recording expenses, managing credit/debit cards, and monitoring savings. It supports recurring charges, generates visual graphs to highlight spending trends, and offers an all-in-one dashboard for easy navigation. All data is stored securely in a local JSON file, allowing the app to run fully offline.

---

##Dependencies

The application requires the following external Python libraries:

- `customtkinter`
- `matplotlib`
- `pandas`
- `python-dateutil`
- `pillow`

----
##To Run  
Install dependencies with:  
pip install -r requirements.txt

Application runs from 
							python UI.py

--

#File Structure & Overview

BrokeBuddy/  
│  
├── logic/                 # Core backend logic  
│   ├── auth.py            # Handles user authentication and login  
│   ├── budget.py          # Budget calculations and limit logic  
│   ├── charts.py          # Creates graphs for spending insights  
│   ├── models.py          # OOP classes: User, Card, Expense  
│   ├── resetter.py        # Handles new month resets  
│   ├── savings.py         # Calculates savings  
│   └── storage.py         # Loads and saves user data to JSON  
│
├── views/                 # All GUI Frames (CustomTkinter-based)  
│   ├── account.py  
│   ├── budgetFrame.py  
│   ├── cards.py  
│   ├── dashboard.py  
│   ├── ExpensesFrame.py  
│   ├── ForgotFrame.py  
│   ├── graphs.py  
│   ├── income.py  
│   ├── LogInSignUp.py  
│   ├── recurrent.py  
│   ├── savings.py  
│   ├── SignIn.py  
│   ├── SignUp.py  
│   └── welcomeFrame.py  
│  
├── Data.json              # Main local data storage file  
├── menu.py                # Used during early terminal testing  
├── UI.py                  # Launches the main window and controls navigation  
├── requirements.txt       # Lists required Python packages  



--

#Bugs and Limitations  
The Console Menu Playground in menu.py does not fully work anymore due to new changes to the data model

