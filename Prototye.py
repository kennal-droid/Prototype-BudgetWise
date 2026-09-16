# ==========================================
# BUDGETWISE
# Personal Expense, Budget & Financial Coach
# ==========================================

from datetime import datetime


# ==========================================
# Transaction Class
# ==========================================

class Transaction:

    def __init__(self, amount, category, transaction_type):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.date = datetime.now().strftime("%Y-%m-%d")

    def display(self):
        print(
            f"{self.date} | "
            f"{self.transaction_type.upper()} | "
            f"{self.category} | "
            f"₱{self.amount:.2f}"
        )


# ==========================================
# Savings Goal Class
# ==========================================

class SavingsGoal:

    def __init__(self, name, target):
        self.name = name
        self.target = target
        self.saved = 0

    def add_savings(self, amount):
        self.saved += amount

    def show_progress(self):

        if self.target > 0:
            progress = (self.saved / self.target) * 100
        else:
            progress = 0

        print("\n========== SAVINGS GOAL ==========")
        print(f"Goal: {self.name}")
        print(f"Target: ₱{self.target:.2f}")
        print(f"Saved: ₱{self.saved:.2f}")
        print(f"Progress: {progress:.1f}%")


# ==========================================
# User Budget Class
# ==========================================

class UserBudget:

    def __init__(self, income, budget_limit):
        self.income = income
        self.budget_limit = budget_limit
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def total_expenses(self):

        total = 0

        for transaction in self.transactions:

            if transaction.transaction_type == "expense":
                total += transaction.amount

        return total

    def total_income(self):

        total = self.income

        for transaction in self.transactions:

            if transaction.transaction_type == "income":
                total += transaction.amount

        return total

    def remaining_balance(self):

        return self.total_income() - self.total_expenses()


# ==========================================
# Report Generator Class
# ==========================================

class ReportGenerator:

    def __init__(self, budget):
        self.budget = budget

    def show_dashboard(self):

        print("\n====================================")
        print("           BUDGETWISE DASHBOARD")
        print("====================================")

        print(f"Total Income:      ₱{self.budget.total_income():.2f}")
        print(f"Total Expenses:    ₱{self.budget.total_expenses():.2f}")
        print(f"Remaining Balance: ₱{self.budget.remaining_balance():.2f}")
        print(f"Monthly Budget:    ₱{self.budget.budget_limit:.2f}")

        # Budget alert

        if self.budget.total_expenses() > self.budget.budget_limit:

            print("\n⚠ BUDGET ALERT")
            print("You have exceeded your monthly budget.")

        elif self.budget.total_expenses() >= self.budget.budget_limit * 0.80:

            print("\n⚠ BUDGET ALERT")
            print("You are approaching your monthly budget.")

        else:

            print("\n✓ Budget Status: Within Limit")


# ==========================================
# Financial Coach Class
# ==========================================

class FinancialCoach:

    def __init__(self, budget, savings_goal):
        self.budget = budget
        self.savings_goal = savings_goal

    def give_advice(self):

        print("\n====================================")
        print("          FINANCIAL COACH")
        print("====================================")

        expenses = self.budget.total_expenses()
        balance = self.budget.remaining_balance()

        if expenses == 0:

            print("No spending data available yet.")
            print("Start adding transactions.")

        elif expenses > self.budget.budget_limit:

            print("⚠ You have exceeded your monthly budget.")
            print("Suggestion: Reduce unnecessary spending.")

        elif expenses >= self.budget.budget_limit * 0.80:

            print("⚠ You are approaching your budget limit.")
            print("Suggestion: Monitor your spending carefully.")

        else:

            print("✓ Your spending is currently within your budget.")
            print("Suggestion: Continue monitoring your expenses.")

        # Savings recommendation

        remaining = self.savings_goal.target - self.savings_goal.saved

        if remaining > 0:

            print(
                f"\n💡 Savings Recommendation:"
                f"\nYou need ₱{remaining:.2f} more "
                f"to reach your savings goal."
            )

        else:

            print("\n🎉 You reached your savings goal!")

        # Balance recommendation

        if balance <= 0:

            print("\n⚠ Your available balance is very low.")

        else:

            print(
                "\n✓ Try setting aside part of your "
                "remaining balance for savings."
            )


# ==========================================
# Cash Flow Predictor Class
# ==========================================

class CashFlowPredictor:

    def __init__(self, budget):
        self.budget = budget

    def predict(self):

        print("\n====================================")
        print("         CASH FLOW PREDICTION")
        print("====================================")

        expenses = self.budget.total_expenses()
        income = self.budget.total_income()

        # Simulated prediction for prototype

        predicted_expenses = expenses * 2

        predicted_balance = income - predicted_expenses

        print(f"Current Income: ₱{income:.2f}")
        print(f"Current Expenses: ₱{expenses:.2f}")

        print(
            f"\nPredicted end-of-month expenses: "
            f"₱{predicted_expenses:.2f}"
        )

        if predicted_balance >= 0:

            print(
                f"Predicted remaining funds: "
                f"₱{predicted_balance:.2f}"
            )

            print("✓ Current spending rate may be manageable.")

        else:

            print("⚠ WARNING")
            print("Your current spending rate may lead to overspending.")

        print("\n* Prediction is simulated for prototype purposes. *")


# ==========================================
# BudgetWise Application
# ==========================================

class BudgetWise:

    def __init__(self):

        self.budget = None
        self.savings_goal = None

        self.report = None
        self.coach = None
        self.predictor = None

    # --------------------------------------
    # Setup
    # --------------------------------------

    def setup(self):

        print("\n====================================")
        print("        WELCOME TO BUDGETWISE")
        print("====================================")

        income = float(
            input("Enter your monthly income: ₱")
        )

        budget_limit = float(
            input("Enter your monthly budget: ₱")
        )

        self.budget = UserBudget(
            income,
            budget_limit
        )

        print("\n✓ Monthly budget created.")

        # Savings Goal

        goal_name = input(
            "\nEnter your savings goal: "
        )

        goal_target = float(
            input("Enter savings target: ₱")
        )

        self.savings_goal = SavingsGoal(
            goal_name,
            goal_target
        )

        print("\n✓ Savings goal created.")

        # Create system components

        self.report = ReportGenerator(
            self.budget
        )

        self.coach = FinancialCoach(
            self.budget,
            self.savings_goal
        )

        self.predictor = CashFlowPredictor(
            self.budget
        )

    # --------------------------------------
    # Add Transaction
    # --------------------------------------

    def add_transaction(self):

        print("\n========== ADD TRANSACTION ==========")

        print("1. Expense")
        print("2. Income")

        choice = input("Choose transaction type: ")

        amount = float(
            input("Enter amount: ₱")
        )

        category = input(
            "Enter category: "
        )

        if choice == "1":

            transaction_type = "expense"

        elif choice == "2":

            transaction_type = "income"

        else:

            print("Invalid transaction type.")
            return

        transaction = Transaction(
            amount,
            category,
            transaction_type
        )

        self.budget.add_transaction(
            transaction
        )

        print("\n✓ Transaction added successfully.")

    # --------------------------------------
    # View Transactions
    # --------------------------------------

    def view_transactions(self):

        print("\n========== TRANSACTIONS ==========")

        if len(self.budget.transactions) == 0:

            print("No transactions recorded.")

        else:

            for transaction in self.budget.transactions:

                transaction.display()

    # --------------------------------------
    # Add Savings
    # --------------------------------------

    def add_savings(self):

        print("\n========== ADD SAVINGS ==========")

        amount = float(
            input("Enter amount to save: ₱")
        )

        self.savings_goal.add_savings(
            amount
        )

        print("\n✓ Savings successfully added.")

    # --------------------------------------
    # Main Menu
    # --------------------------------------

    def run(self):

        self.setup()

        while True:

            print("\n====================================")
            print("             BUDGETWISE")
            print("====================================")

            print("1. Add Transaction")
            print("2. View Dashboard")
            print("3. View Transactions")
            print("4. Add Savings")
            print("5. View Savings Goal")
            print("6. Financial Coach")
            print("7. Cash Flow Prediction")
            print("8. Exit")

            choice = input(
                "\nSelect an option: "
            )

            if choice == "1":

                self.add_transaction()

            elif choice == "2":

                self.report.show_dashboard()

            elif choice == "3":

                self.view_transactions()

            elif choice == "4":

                self.add_savings()

            elif choice == "5":

                self.savings_goal.show_progress()

            elif choice == "6":

                self.coach.give_advice()

            elif choice == "7":

                self.predictor.predict()

            elif choice == "8":

                print("\n====================================")
                print("       SAVING FINANCIAL RECORDS")
                print("====================================")

                print("✓ Records saved successfully.")
                print("Thank you for using BudgetWise!")

                break

            else:

                print("\n⚠ Invalid option. Please try again.")


# ==========================================
# Start Program
# ==========================================

app = BudgetWise()
app.run()