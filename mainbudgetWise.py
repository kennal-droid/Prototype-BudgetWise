import streamlit as st
from userBudgetWise import userBudgetWise
from transactions import transactions
from UserBudget import UserBudget
from SavingsGoal import SavingsGoal
from Category import Category
from FinancialCoach import FinancialCoach
from supabaseClient import supabase

st.set_page_config(page_title="BudgetWise", page_icon="💰", layout="wide")

# ---------------------------------------------------------
# 1. Authentication & Session State Setup
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

def show_login_page():
    st.title("💰 BudgetWise")
    st.caption("Personal Expense, Budget & Financial Coach")
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
        
        # --- LOGIN TAB ---
        with tab1:
            st.subheader("Login to Your Account")
            with st.form("login_form"):
                login_id = st.text_input("User ID (e.g. U101)")
                submit_login = st.form_submit_button("Login")
                
                if submit_login:
                    if login_id.strip():
                        try:
                            # Fetch user from Supabase
                            response = supabase.table("users").select("*").eq("user_id", login_id.strip()).execute()
                            if response.data:
                                db_user = response.data[0]
                                st.session_state.user = userBudgetWise(
                                    userID=db_user["user_id"],
                                    name=db_user["name"],
                                    monthlyIncome=float(db_user["monthly_income"])
                                )
                                st.session_state.authenticated = True
                                st.success(f"Welcome back, {db_user['name']}!")
                                st.rerun()
                            else:
                                st.error("User ID not found. Please check your ID or sign up.")
                        except Exception as e:
                            st.error(f"Database connection error: {e}")
                    else:
                        st.warning("Please enter a valid User ID.")

        # --- SIGNUP TAB ---
        with tab2:
            st.subheader("Create a New Account")
            with st.form("signup_form"):
                new_id = st.text_input("Choose User ID (e.g. U102)")
                new_name = st.text_input("Full Name")
                new_income = st.number_input("Monthly Income (₱)", min_value=0.0, value=25000.0, step=1000.0)
                submit_signup = st.form_submit_button("Create Account")
                
                if submit_signup:
                    if new_id.strip() and new_name.strip():
                        try:
                            # Register user in Supabase
                            supabase.table("users").insert({
                                "user_id": new_id.strip(),
                                "name": new_name.strip(),
                                "monthly_income": new_income
                            }).execute()
                            
                            # Initialize instance
                            st.session_state.user = userBudgetWise(
                                userID=new_id.strip(),
                                name=new_name.strip(),
                                monthlyIncome=new_income
                            )
                            st.session_state.authenticated = True
                            st.success("Account created successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to create account: {e}")
                    else:
                        st.warning("Please provide both a User ID and Name.")

# Block access until authenticated
if not st.session_state.authenticated or st.session_state.user is None:
    show_login_page()
    st.stop()

# ---------------------------------------------------------
# 2. Main Dashboard (Authenticated User Area)
# ---------------------------------------------------------
user = st.session_state.user

st.title("BudgetWise")
st.caption("Personal Expense, Budget & Financial Coach")

# --- Sidebar Controls ---
st.sidebar.header(f"👤 {user.name}")
st.sidebar.caption(f"User ID: {user.userID}")

# Editable Profile Fields
name_input = st.sidebar.text_input("Name", value=user.name)
income_input = st.sidebar.number_input("Monthly Income (₱)", min_value=0.0, value=user.monthlyIncome, step=1000.0)

user.name = name_input
user.monthlyIncome = income_input

# Cloud Sync Button
if st.sidebar.button("Sync Profile to Cloud"):
    try:
        supabase.table("users").upsert({
            "user_id": user.userID,
            "name": user.name,
            "monthly_income": user.monthlyIncome
        }).execute()
        st.sidebar.success("Profile saved to database!")
    except Exception as e:
        st.sidebar.error(f"Cloud sync failed: {e}")

if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.session_state.user = None
    st.rerun()

menu = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Add Expense", "View Expenses", "Manage Budget", "Saving Goals", "Financial Coach"]
)

# --- Dashboard ---
if menu == "Dashboard":
    st.header(f"Welcome back, {user.name}!")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("User ID", user.userID)
    col2.metric("Monthly Income", f"₱{user.monthlyIncome:,.2f}")
    col3.metric("Total Transactions", len(user.transactions))

# --- Add Expense ---
elif menu == "Add Expense":
    st.header("💳 Add New Expense")
    
    with st.form("add_expense_form", clear_on_submit=True):
        expense_name = st.text_input("Expense Description (e.g. Groceries)")
        category = st.selectbox("Category", ["Food & Dining", "Transportation", "Utilities", "Entertainment", "Shopping", "General"])
        expense_amount = st.number_input("Amount (₱)", min_value=0.01, step=50.0)
        transaction_id = st.text_input("Transaction ID", value=f"TXN{len(user.transactions)+1:03d}")
        
        submitted = st.form_submit_button("Record Expense")
        if submitted:
            if expense_name:
                new_tx = transactions(
                    amount=expense_amount, 
                    transactionID=transaction_id, 
                    type="expense", 
                    category=category, 
                    description=expense_name
                )
                user.addtransaction(new_tx)
                st.success(f"Added expense: {expense_name} ({category}) - ₱{expense_amount:,.2f}")
            else:
                st.warning("Please provide an expense description.")

# --- View Expenses ---
elif menu == "View Expenses":
    st.header("📊 Transaction History")
    
    if user.transactions:
        for tx in user.transactions:
            category_label = getattr(tx, "category", "General")
            description_label = getattr(tx, "description", "No description")
            st.write(
                f"**Date:** {tx.date} | **Type:** {tx.type.upper()} | "
                f"**Category:** [{category_label}] | **ID:** {tx.transactionID} | "
                f"**Amount:** ₱{tx.amount:,.2f} | **Desc:** {description_label}"
            )
    else:
        st.info("No expenses recorded yet.")

# --- Manage Budget ---
elif menu == "Manage Budget":
    st.header("🎯 Budget Management")
    
    monthly_limit = st.number_input("Monthly Expense Limit (₱)", min_value=0.0, value=15000.0, step=500.0)
    current_spending = user.getTotalExpenses()
    
    budget = UserBudget("B001", monthly_limit, current_spending)
    budget.calculateRemaining()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly Limit", f"₱{budget.monthlyLimit:,.2f}")
    col2.metric("Current Spending", f"₱{budget.currentSpending:,.2f}")
    col3.metric("Remaining Budget", f"₱{budget.remainingBudget:,.2f}")
    
    st.subheader("Status")
    st.info(budget.checkBudgetStatus())

# --- Saving Goals ---
elif menu == "Saving Goals":
    st.header("🎯 Savings Goal Tracker")
    
    with st.form("savings_form"):
        goal_id = st.text_input("Goal ID", value="G001")
        goal_name = st.text_input("Goal Name", value="Emergency Fund")
        target_amount = st.number_input("Target Amount (₱)", min_value=1.0, value=50000.0, step=1000.0)
        current_savings = st.number_input("Current Savings (₱)", min_value=0.0, value=5000.0, step=500.0)
        
        submitted = st.form_submit_button("Calculate Savings Progress")
        if submitted:
            goal = SavingsGoal(goal_id, goal_name, target_amount, current_savings)
            
            st.subheader(f"Goal: {goal.goalName}")
            st.write(f"**Target:** ₱{goal.targetAmount:,.2f}")
            st.write(f"**Saved:** ₱{goal.currentSavings:,.2f}")
            
            progress = goal.calculateProgress()
            st.progress(min(progress / 100, 1.0))
            st.write(f"**Progress:** {progress:.2f}%")
            st.write(f"**Status:** {goal.checkGoalStatus()}")

# --- Financial Coach ---
elif menu == "Financial Coach":
    st.header("🤖 Financial Coach Advice")
    
    current_spending = user.getTotalExpenses()
    pattern = f"Spent ₱{current_spending:,.2f} out of ₱{user.monthlyIncome:,.2f} income."
    
    if current_spending > user.monthlyIncome * 0.8:
        rec = "You are spending more than 80% of your income. Focus on cutting non-essential costs."
    else:
        rec = "Your spending is healthy. Consider channeling extra balance into savings!"
        
    coach = FinancialCoach(rec, pattern)
    
    st.subheader("Spending Pattern Analysis")
    st.write(coach.analyzeSpending())
    
    st.subheader("Recommendation")
    st.success(coach.giveSuggestion())