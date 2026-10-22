# BudgetWise

## Project Description

BudgetWise is an object-oriented personal expense management system designed for college students. It helps users manage their finances by tracking income and expenses, monitoring budgets, setting savings goals, and receiving financial suggestions based on their spending habits.

The project uses Python and Streamlit to provide an interactive user interface. It also integrates with Supabase for cloud database functionality.

## Important Features

- **Expense Tracking:** Record and manage income and expenses.
- **Budget Management:** Set spending limits and monitor remaining budgets.
- **Savings Goals:** Set financial targets and track savings progress.
- **Financial Coach:** Receive predefined suggestions based on spending habits and budget status.
- **Expense Filtering:** View and organize transactions by supported date ranges.
- **Interactive Dashboard:** View financial information through a Streamlit interface.
- **Cloud Database Integration:** Store and synchronize supported user and transaction data through Supabase.
- **Object-Oriented Architecture:** Organize project functionality into separate Python classes.

## Object-Oriented Programming Implementation

BudgetWise uses Object-Oriented Programming (OOP) to organize its code into classes with distinct responsibilities.

### OOP Principles

- **Encapsulation:** Organizes data and related methods within classes to manage object state.
- **Abstraction:** Separates implementation details from the operations used by other parts of the application.
- **Modularity:** Divides the application into classes and modules to improve code organization and maintainability.

### Main Classes

- **`userBudgetWise`:** Manages user profile information and related user operations.
- **`transactions`:** Handles financial transaction records and supported filtering operations.
- **`UserBudget`:** Manages budget limits, spending, and remaining balances.
- **`SavingsGoal`:** Manages savings targets and progress.
- **`Category`:** Organizes transactions into categories.
- **`FinancialCoach`:** Analyzes spending information and provides predefined financial suggestions.

Each class contributes to a specific part of the application's financial management functionality.

## Technologies Used

- **Python:** Main programming language.
- **Streamlit:** Interactive user interface.
- **Supabase:** Cloud database and data synchronization, where configured.
- **Git and GitHub:** Source code management and project hosting.

## Requirements

Before running BudgetWise, make sure you have:

- Python installed on your computer.
- The project source code cloned from GitHub.
- The required Python packages listed in `requirements.txt`.
- A Supabase project and the required database configuration if you want to use cloud features.

## Setup Instructions

### 1. Clone the Repository

Open a terminal or command prompt and run:

```bash
git clone https://github.com/kennal-droid/Prototype-BudgetWise.git
cd Prototype-BudgetWise
```

### 2. Create a Virtual Environment

Create an isolated Python environment for the project:

```bash
python -m venv .venv
```

On Windows, activate it using:

```bash
.venv\Scripts\activate
```

On macOS or Linux, activate it using:

```bash
source .venv/bin/activate
```

If the `python` command is unavailable on Windows, you can try `py` instead.

### 3. Install Dependencies

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Supabase

If your local application requires Supabase, configure your credentials using the method expected by your source code.

For example, if your application reads credentials from Streamlit secrets, create a file at:

`.streamlit/secrets.toml`

Add the following structure, replacing the placeholders with your own credentials:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-supabase-key"
```

**Important:** The configuration names above are examples. Confirm that they match the names read by your `supabaseClient.py` file. Configure the required Supabase database tables and permissions according to your application's implementation.

Do not commit real credentials or private keys to GitHub.

### 5. Run the Application

From the project directory, run:

```bash
streamlit run mainbudgetWise.py
```

This command assumes that `mainbudgetWise.py` is the main Streamlit application file. If your actual entry-point file is different, replace the filename with the correct one.

## Security and Credentials

- Keep Supabase keys, passwords, and other sensitive information private.
- Store credentials in local configuration files or environment variables as supported by the application.
- Ensure `.env` and `.streamlit/secrets.toml` are excluded from version control when they contain real credentials.
- Review changes before pushing them to GitHub to ensure no secrets are included.
- Use appropriate Supabase permissions and Row Level Security (RLS) policies where applicable.
- Never expose a Supabase service-role key in a public repository or client-side application.

## Project Repository

GitHub: https://github.com/kennal-droid/Prototype-BudgetWise

## Project Purpose

BudgetWise aims to help college students develop better financial management habits by making it easier to monitor expenses, manage budgets, and work toward savings goals.
