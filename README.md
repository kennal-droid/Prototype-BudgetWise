BudgetWise
BudgetWise is an object-oriented personal expense management system designed specifically for college students. It addresses the common challenge of unpredictable student allowances and end-of-month financial crunches by providing real-time tracking, automated budgeting alerts, and secure cloud synchronization.

Important Features
Modular Object-Oriented Architecture: Clean separation of data models and business logic across dedicated Python classes.

Real-Time Expense Filtering: Dynamic daily, weekly, and monthly views with automated warning indicators for critical spending limits.

Cloud Sync & Persistence: Automated background upsert operations syncing user profiles and transaction streams securely via Supabase.

Secure Account Recovery: Multi-tier verification matching exact usernames, income ranges, and transaction tie-breakers.

Interactive Streamlit Dashboard: A responsive, user-friendly UI designed for seamless everyday financial management.

OOP Implementation
BudgetWise implements core Object-Oriented Programming (OOP) principles to maintain clean, scalable, and maintainable code:

Encapsulation: Internal attributes and state management are protected and controlled through explicit methods within each model class.

Abstraction: Complex database queries and Supabase connection handling are abstracted away from the core UI components.

Modular Class Structure:

userBudgetWise: Manages user authentication and profile data.

transactions: Handles income, expense records, and dynamic filtering.

UserBudget: Manages user budget limits and allocations.

SavingsGoal: Tracks personal savings targets.

Category: Organizes financial entries into logical groupings.

FinancialCoach: Evaluates user spending habits and triggers automated alerts.

Setup Instructions
Prerequisites
Python 3.8 or higher installed on your system.

A Supabase project with configured database tables for users and transactions.

Installation & Configuration Steps
Clone the Repository:

Bash
git clone https://github.com/kennal-droid/Prototype-BudgetWise.git
cd Prototype-BudgetWise
Set Up a Virtual Environment (Recommended):

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install Dependencies:
Install all required project dependencies using the provided requirements.txt file:

Bash
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file or Streamlit secrets configuration (.streamlit/secrets.toml) to store your private Supabase credentials safely without hardcoding them into source files.

Example .streamlit/secrets.toml:

Ini, TOML
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-or-service-role-key-here"
Run the Application:
Launch the Streamlit dashboard locally:

Bash
streamlit run app.py
Security & Credentials
Credential Protection: Private API keys, database URLs, and user passwords are kept out of source control using local configuration secrets (.streamlit/secrets.toml or environment variables) which are ignored by .gitignore.

Repository Check: Before pushing changes, always verify that your .env or sensitive secret files are not accidentally staged or committed to GitHub.
