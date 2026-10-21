import datetime
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
# Helper: Load User Transactions from Supabase
# ---------------------------------------------------------
def load_user_transactions(user_obj):
    """Fetches user transactions from Supabase and populates the local object."""
    try:
        tx_response = supabase.table("transactions").select("*").eq("user_id", user_obj.userID).execute()
        if tx_response.data:
            # Clear local list to avoid duplicate appends on reload
            user_obj.transactions = []
            for row in tx_response.data:
                stored_date = row.get("created_at", str(datetime.date.today()))
                if "T" in stored_date:
                    stored_date = stored_date.split("T")[0]
                    
                loaded_tx = transactions(
                    amount=float(row["amount"]),
                    transactionID=row["transaction_id"],
                    type=row.get("type", "expense"),
                    category=row.get("category", "General"),
                    description=row.get("description", "No description")
                )
                loaded_tx.date = stored_date
                user_obj.addtransaction(loaded_tx)
    except Exception as e:
        st.sidebar.error(f"Could not load cloud transactions: {e}")

# ---------------------------------------------------------
# 1. Authentication & Session State Setup
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "savings_goals" not in st.session_state:
    st.session_state.savings_goals = [
        SavingsGoal("G001", "Emergency Fund", 50000.0, 5000.0)
    ]

def show_login_page():
    st.title("💰 BudgetWise")
    st.caption("Personal Expense, Budget & Financial Coach")
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2, tab3 = st.tabs(["🔑 Login", "📝 Sign Up", "🔍 Forgot ID"])
        
        # --- LOGIN TAB (Updated with Dual Verification: ID + Name) ---
        with tab1:
            st.subheader("Login to Your Account")
            with st.form("login_form"):
                login_id = st.text_input("User ID (e.g. U101)")
                login_name = st.text_input("Registered Full Name")
                submit_login = st.form_submit_button("Login")
                
                if submit_login:
                    if login_id.strip() and login_name.strip():
                        try:
                            response = supabase.table("users").select("*").eq("user_id", login_id.strip()).execute()
                            if response.data:
                                db_user = response.data[0]
                                
                                # Verify if the entered name matches the database record
                                if db_user["name"].strip().lower() == login_name.strip().lower():
                                    user_instance = userBudgetWise(
                                        userID=db_user["user_id"],
                                        name=db_user["name"],
                                        monthlyIncome=float(db_user["monthly_income"])
                                    )
                                    load_user_transactions(user_instance)
                                    
                                    st.session_state.user = user_instance
                                    st.session_state.authenticated = True
                                    st.success(f"Welcome back, {db_user['name']}!")
                                    st.rerun()
                                else:
                                    st.error("The Name provided does not match this User ID. Please check your credentials.")
                            else:
                                st.error("User ID not found. Please check your ID or sign up.")
                        except Exception as e:
                            st.error(f"Database connection error: {e}")
                    else:
                        st.warning("Please enter both your User ID and Full Name.")

        # --- SIGNUP TAB ---
        with tab2:
            st.subheader("Create or Update Account")
            with st.form("signup_form"):
                new_id = st.text_input("Choose User ID (e.g. U102)")
                new_name = st.text_input("Full Name")
                new_income = st.number_input("Monthly Income (₱)", min_value=0.0, value=25000.0, step=1000.0)
                submit_signup = st.form_submit_button("Register / Save Account")
                
                if submit_signup:
                    if new_id.strip() and new_name.strip():
                        try:
                            supabase.table("users").upsert({
                                "user_id": new_id.strip(),
                                "name": new_name.strip(),
                                "monthly_income": new_income
                            }, on_conflict="user_id").execute()
                            
                            user_instance = userBudgetWise(
                                userID=new_id.strip(),
                                name=new_name.strip(),
                                monthlyIncome=new_income
                            )
                            load_user_transactions(user_instance)
                            
                            st.session_state.user = user_instance
                            st.session_state.authenticated = True
                            st.success("Account saved successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to save account: {e}")
                    else:
                        st.warning("Please provide both a User ID and Name.")

        # --- FIND ID TAB (With Collision Handling) ---
        with tab3:
            st.subheader("🔍 Forgot User ID?")
            search_name = st.text_input("Enter your registered Full Name")
            
            if st.button("Search Account"):
                if search_name.strip():
                    matches = userBudgetWise.find_users_by_name(search_name)
                    if not matches:
                        st.error("No account found with that name.")
                    elif len(matches) == 1:
                        m = matches[0]
                        st.success(f"Found Account: **{m['name']}** → User ID: **`{m['user_id']}`**")
                    else:
                        st.session_state.found_matches = matches
                        st.warning(f"Found {len(matches)} accounts with the name '{search_name}'. Please verify your profile below.")
                else:
                    st.warning("Please enter a name to search.")

            # Disambiguation Prompt for Duplicate Names
            if "found_matches" in st.session_state and st.session_state.found_matches:
                st.write("---")
                st.subheader("Identity Verification")
                verify_income = st.number_input("Enter your registered Monthly Income (₱) to verify:", min_value=0.0, step=500.0, key="verify_income_input")
                
                if st.button("Verify Identity"):
                    matched_user = None
                    for m in st.session_state.found_matches:
                        if abs(float(m["monthly_income"]) - verify_income) < 1.0:
                            matched_user = m
                            break
                    
                    if matched_user:
                        st.success(f"Identity Verified! Welcome **{matched_user['name']}** → Your User ID is **`{matched_user['user_id']}`**")
                        del st.session_state.found_matches
                    else:
                        st.error("Income value does not match any account with that name. Please check your input.")

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

name_input = st.sidebar.text_input("Name", value=user.name)
income_input = st.sidebar.number_input("Monthly Income (₱)", min_value=0.0, value=user.monthlyIncome, step=1000.0)

if name_input != user.name or income_input != user.monthlyIncome:
    user.name = name_input
    user.monthlyIncome = income_input
    try:
        supabase.table("users").upsert({
            "user_id": user.userID,
            "name": user.name,
            "monthly_income": user.monthlyIncome
        }, on_conflict="user_id").execute()
        st.sidebar.success("Profile auto-synced!")
    except Exception as e:
        st.sidebar.error(f"Auto-sync failed: {e}")

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
    
    current_spending = user.getTotalExpenses()
    remaining_balance = user.monthlyIncome - current_spending
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Monthly Income", f"₱{user.monthlyIncome:,.2f}")
    col2.metric("Total Spending", f"₱{current_spending:,.2f}")
    col3.metric("Net Balance", f"₱{remaining_balance:,.2f}")
    col4.metric("Total Transactions", len(user.transactions))
    
    st.write("---")
    st.subheader("Quick Financial Overview")
    
    if current_spending > user.monthlyIncome:
        st.error("🚨 CRITICAL ALERT: Your total spending currently exceeds your monthly income!")
    elif current_spending > user.monthlyIncome * 0.8:
        st.error("⚠️ CAUTION: You have spent over 80% of your monthly income.")
    else:
        st.success("✅ Your spending is within a healthy range relative to your income.")

# --- Add Expense ---
elif menu == "Add Expense":
    st.header("💳 Add New Expense")
    
    with st.form("add_expense_form", clear_on_submit=True):
        expense_name = st.text_input("Expense Description (e.g. Groceries)")
        category = st.selectbox("Category", ["Food & Dining", "Transportation", "Utilities", "Entertainment", "Shopping", "General"])
        expense_amount = st.number_input("Amount (₱)", min_value=0.01, step=50.0)
        expense_date = st.date_input("Transaction Date", value=datetime.date.today())
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
                new_tx.date = str(expense_date)
                user.addtransaction(new_tx)
                
                try:
                    supabase.table("transactions").insert({
                        "user_id": user.userID,
                        "transaction_id": transaction_id,
                        "amount": expense_amount,
                        "type": "expense",
                        "category": category,
                        "description": expense_name,
                        "created_at": str(expense_date)
                    }).execute()
                    st.success(f"Added & synced expense: {expense_name} ({category}) on {expense_date} - ₱{expense_amount:,.2f}")
                except Exception as db_err:
                    st.error(f"Saved locally, but cloud sync failed: {db_err}")
            else:
                st.warning("Please provide an expense description.")

# --- View Expenses ---
elif menu == "View Expenses":
    st.header("📊 Transaction History")
    
    if user.transactions:
        view_mode = st.radio("Filter By Period Preference", ["All", "Daily", "Weekly", "Monthly"], horizontal=True)
        
        filtered_transactions = []
        today = datetime.date.today()
        
        for tx in user.transactions:
            try:
                tx_date = datetime.date.fromisoformat(str(tx.date))
            except Exception:
                tx_date = today
                
            if view_mode == "All":
                filtered_transactions.append((tx_date, tx))
            elif view_mode == "Daily":
                if tx_date == today:
                    filtered_transactions.append((tx_date, tx))
            elif view_mode == "Weekly":
                if tx_date.isocalendar()[1] == today.isocalendar()[1] and tx_date.year == today.year:
                    filtered_transactions.append((tx_date, tx))
            elif view_mode == "Monthly":
                if tx_date.month == today.month and tx_date.year == today.year:
                    filtered_transactions.append((tx_date, tx))
        
        period_total = sum(tx.amount for _, tx in filtered_transactions)
        
        st.write("---")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric(f"{view_mode} Total Spending", f"₱{period_total:,.2f}")
        col_m2.metric("Filtered Records", len(filtered_transactions))
        st.write("---")
        
        if filtered_transactions:
            for tx_date, tx in filtered_transactions:
                category_label = getattr(tx, "category", "General")
                description_label = getattr(tx, "description", "No description")
                st.write(
                    f"**Date:** {tx.date} | **Type:** {tx.type.upper()} | "
                    f"**Category:** [{category_label}] | **ID:** {tx.transactionID} | "
                    f"**Amount:** ₱{tx.amount:,.2f} | **Desc:** {description_label}"
                )
        else:
            st.info(f"No transactions found for the selected '{view_mode}' filter.")
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
    if budget.remainingBudget < 0:
        st.error(f"🚨 BUDGET EXCEEDED! You are over budget by ₱{abs(budget.remainingBudget):,.2f}.")
    elif budget.currentSpending > budget.monthlyLimit * 0.8:
        st.error(f"⚠️ Warning: You have used over 80% of your monthly budget limit!")
    else:
        st.info(budget.checkBudgetStatus())

# --- Saving Goals ---
elif menu == "Saving Goals":
    st.header("🎯 Savings Goal Tracker")
    
    with st.expander("➕ Create a New Savings Goal", expanded=False):
        with st.form("savings_form", clear_on_submit=True):
            goal_id = st.text_input("Goal ID", value=f"G{len(st.session_state.savings_goals)+1:03d}")
            goal_name = st.text_input("Goal Name (e.g. New Laptop)")
            target_amount = st.number_input("Target Amount (₱)", min_value=1.0, value=10000.0, step=1000.0)
            current_savings = st.number_input("Initial Savings (₱)", min_value=0.0, value=0.0, step=500.0)
            
            submitted = st.form_submit_button("Add Goal")
            if submitted:
                if goal_name.strip():
                    new_goal = SavingsGoal(goal_id, goal_name, target_amount, current_savings)
                    st.session_state.savings_goals.append(new_goal)
                    st.success(f"Successfully added goal: {goal_name}!")
                    st.rerun()
                else:
                    st.warning("Please provide a Goal Name.")

    st.write("---")
    st.subheader("Your Active Savings Goals")
    
    if st.session_state.savings_goals:
        for idx, goal in enumerate(st.session_state.savings_goals):
            col_header1, col_header2 = st.columns([4, 1])
            col_header1.write(f"### 🎯 {goal.goalName} (`{goal.goalID}`)")
            
            if col_header2.button("🗑️ Delete", key=f"del_{idx}"):
                st.session_state.savings_goals.pop(idx)
                st.success(f"Deleted goal: {goal.goalName}")
                st.rerun()

            col_g1, col_g2 = st.columns(2)
            col_g1.write(f"**Target:** ₱{goal.targetAmount:,.2f}")
            col_g2.write(f"**Saved:** ₱{goal.currentSavings:,.2f}")
            
            progress = goal.calculateProgress()
            st.progress(min(progress / 100, 1.0))
            st.write(f"**Progress:** {progress:.2f}% | **Status:** {goal.checkGoalStatus()}")
            
            with st.form(key=f"deposit_form_{idx}"):
                col_d1, col_d2 = st.columns([2, 1])
                deposit_amount = col_d1.number_input(f"Add Funds (₱)", min_value=0.0, step=100.0, key=f"dep_{idx}")
                deposit_submitted = col_d2.form_submit_button("Deposit Money")
                if deposit_submitted:
                    if deposit_amount > 0:
                        goal.currentSavings += deposit_amount
                        st.success(f"Added ₱{deposit_amount:,.2f} to {goal.goalName}!")
                        st.rerun()
                    else:
                        st.warning("Enter a valid amount to deposit.")
            st.write("---")
    else:
        st.info("No savings goals created yet.")

# --- Financial Coach ---
elif menu == "Financial Coach":
    st.header("🤖 Financial Coach Advice")
    
    current_spending = user.getTotalExpenses()
    pattern = f"Spent ₱{current_spending:,.2f} out of ₱{user.monthlyIncome:,.2f} income."
    
    if current_spending > user.monthlyIncome:
        rec = "CRITICAL ALERT: Your expenses exceed your monthly income! Immediate budget cuts are required."
    elif current_spending > user.monthlyIncome * 0.8:
        rec = "You are spending more than 80% of your income. Focus on cutting non-essential costs immediately."
    else:
        rec = "Your spending is healthy. Consider channeling extra balance into savings!"
        
    coach = FinancialCoach(rec, pattern)
    
    st.subheader("Spending Pattern Analysis")
    st.write(coach.analyzeSpending())
    
    st.subheader("Recommendation")
    if current_spending > user.monthlyIncome * 0.8:
        st.error(coach.giveSuggestion())
    else:
        st.success(coach.giveSuggestion())
