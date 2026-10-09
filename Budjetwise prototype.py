from datetime import datetime


# -----------------------------
# Transaction Class
# -----------------------------
class Transaction:
    def __init__(self, amount, category, transaction_type, date=None):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def display(self):
        print(
            f"{self.date} | {self.transaction_type.upper()} | "
            f"{self.category} | ₱{self.amount:.2f}"
        )


# -----------------------------
# User Budget Class
# -----------------------------
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

    def category_total(self, category):
        total = 0

        for transaction in self.transactions:
            if (
                transaction.transaction_type == "expense"
                and transaction.category.lower() == category.lower()
            ):
                total += transaction.amount

        return total


# -----------------------------
# Savings Goal Class
# -----------------------------
class SavingsGoal:
    def __init__(self, name, target):
        self.name = name
        self.target = target
        self.saved = 0

    def add_savings(self, amount):
        self.saved += amount

    def progress(self):
        if self.target == 0:
            return 0

        return (self.saved / self.target) * 100

    def display(self):
        print("\n--- Savings Goal ---")
        print(f"Goal: {self.name}")
        print(f"Target: ₱{self.target:.2f}")
        print(f"Saved: ₱{self.saved:.2f}")
        print(f"Progress: {self.progress():.1f}%")


# -----------------------------
# Report Generator Class
# -----------------------------
class ReportGenerator:
    def __init__(self, budget):
        self.budget = budget

    def show_summary(self):
        print("\n========== FINANCIAL SUMMARY ==========")
        print(f"Total Income:     ₱{self.budget.total_income():.2f}")
        print(f"Total Expenses:   ₱{self.budget.total_expenses():.2f}")
        print(f"Remaining Balance: ₱{self.budget.remaining_balance():.2f}")
        print(f"Monthly Budget:   ₱{self.budget.budget_limit:.2f}")

        if self.budget.total_expenses() > self.budget.budget_limit:
            print("⚠ WARNING: You exceeded your monthly budget!")
        elif self.budget.total_expenses() >= self.budget.budget_limit * 0.8:
            print("⚠ WARNING: You are approaching your budget limit.")
        else:
            print("✓ You are within your budget.")

    def show_categories(self):
        print("\n========== CATEGORY SPENDING ==========")

        categories = []

        for transaction in self.budget.transactions:
            if transaction.transaction_type == "expense":
                if transaction.category not in categories:
                    categories.append(transaction.category)

        if len(categories) == 0:
            print("No expenses recorded yet.")
            return

        for category in categories:
            amount = self.budget.category_total(category)
            print(f"{category}: ₱{amount:.2f}")


# -----------------------------
# Financial Coach Class
# -----------------------------
class FinancialCoach:
    def __init__(self, budget, savings_goal):
        self.budget = budget
        self.savings_goal = savings_goal

    def give_advice(self):
        print("\n========== FINANCIAL COACH ==========")

        expenses = self.budget.total_expenses()
        balance = self.budget.remaining_balance()
        budget_limit = self.budget.budget_limit

        if expenses == 0:
            print("Start recording your expenses so I can analyze your spending.")
            return

        # Budget advice
        if expenses > budget_limit:
            print("⚠ You have exceeded your monthly budget.")
            print("Suggestion: Reduce unnecessary spending for the rest of the month.")

        elif expenses >= budget_limit * 0.8:
            print("⚠ You are close to reaching your monthly budget.")
            print("Suggestion: Monitor your expenses carefully.")

        else:
            print("✓ Your spending is currently within your monthly budget.")

        # Savings advice
        if self.savings_goal.target > 0:
            remaining_goal = (
                self.savings_goal.target - self.savings_goal.saved
            )

            if remaining_goal > 0:
                print(
                    f"💡 You still need ₱{remaining_goal:.2f} "
                    f"to reach your savings goal."
                )

                if balance > remaining_goal:
                    print(
                        "Suggestion: Your current balance could cover "
                        "the remaining savings target."
                    )
                else:
                    print(
                        "Suggestion: Consider reducing expenses "
                        "to increase your savings."
                    )
            else:
                print("🎉 Congratulations! You reached your savings goal!")

        # General advice
        if balance <= 0:
            print("⚠ Your available balance is very low or negative.")
            print("Suggestion: Avoid unnecessary purchases.")

        elif expenses / self.budget.income >= 0.7:
            print(
                "💡 More than 70% of your income has been spent."
            )
            print(
                "Suggestion: Try setting aside money for savings "
                "before spending."
            )


# -----------------------------
# Main Application
# -----------------------------
def main():

    print("===================================")
    print("        BUDGETWISE")
    print(" Personal Expense & Financial Coach")
    print("===================================")

    # User setup
    income = float(input("\nEnter your monthly income: ₱"))
    budget_limit = float(input("Enter your monthly budget limit: ₱"))

    budget = UserBudget(income, budget_limit)

    # Savings goal
    goal_name = input("Enter your savings goal: ")
    goal_target = float(input("Enter your savings target: ₱"))

    savings_goal = SavingsGoal(goal_name, goal_target)

    report = ReportGenerator(budget)
    coach = FinancialCoach(budget, savings_goal)

    # Main menu
    while True:

        print("\n========== BUDGETWISE MENU ==========")
        print("1. Add Expense")
        print("2. Add Income")
        print("3. View Transactions")
        print("4. View Financial Summary")
        print("5. View Category Spending")
        print("6. Add Savings")
        print("7. View Savings Goal")
        print("8. Financial Coach")
        print("9. Exit")

        choice = input("\nChoose an option: ")

        # Add Expense
        if choice == "1":

            amount = float(input("Enter expense amount: ₱"))
            category = input("Enter category: ")

            transaction = Transaction(
                amount,
                category,
                "expense"
            )

            budget.add_transaction(transaction)

            print("✓ Expense added successfully.")

        # Add Income
        elif choice == "2":

            amount = float(input("Enter income amount: ₱"))
            category = input("Enter income category: ")

            transaction = Transaction(
                amount,
                category,
                "income"
            )

            budget.add_transaction(transaction)

            print("✓ Income added successfully.")

        # View Transactions
        elif choice == "3":

            print("\n========== TRANSACTIONS ==========")

            if len(budget.transactions) == 0:
                print("No transactions recorded.")
            else:
                for transaction in budget.transactions:
                    transaction.display()

        # Financial Summary
        elif choice == "4":
            report.show_summary()

        # Category Spending
        elif choice == "5":
            report.show_categories()

        # Add Savings
        elif choice == "6":

            amount = float(input("Enter amount to save: ₱"))

            savings_goal.add_savings(amount)

            print("✓ Savings added successfully.")

        # Savings Goal
        elif choice == "7":
            savings_goal.display()

        # Financial Coach
        elif choice == "8":
            coach.give_advice()

        # Exit
        elif choice == "9":

            print("\nThank you for using BudgetWise!")
            print("Keep tracking, saving, and spending wisely. 💰")
            break

        else:
            print("Invalid option. Please try again.")


# Run the program
main()