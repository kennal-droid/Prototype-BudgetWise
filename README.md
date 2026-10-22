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
Python 3.8 or higher

A Supabase account and project database
