class userBudgetWise:
    def __init__(self, userID="U101", name="User", monthlyIncome=0.0):
        self.userID = str(userID)
        self.name = str(name)
        self.monthlyIncome = float(monthlyIncome)
        self.transactions = []

    def addtransaction(self, transaction):
        """Adds a transaction if the amount is greater than zero."""
        if hasattr(transaction, "amount") and float(transaction.amount) > 0:
            self.transactions.append(transaction)
            return True
        return False

    def getTotalExpenses(self):
        """Calculates total spent across all expense-type transactions."""
        return sum(tx.amount for tx in self.transactions if getattr(tx, "type", "").lower() == "expense")

    def getTotalIncome(self):
        """Calculates extra earned income across all income-type transactions."""
        return sum(tx.amount for tx in self.transactions if getattr(tx, "type", "").lower() == "income")

    def getRemainingBalance(self):
        """Net Balance = Base Monthly Income + Extra Income - Total Expenses."""
        return self.monthlyIncome + self.getTotalIncome() - self.getTotalExpenses()

    def viewDashboard(self):
        """Terminal preview helper."""
        print("======= Welcome User =======")
        print(f"User ID: {self.userID}")
        print(f"Name: {self.name}")
        print(f"Monthly Income: ₱{self.monthlyIncome:,.2f}")
        print(f"Total Transactions: {len(self.transactions)}")

    @staticmethod
    def find_users_by_name(name_query):
        """Class/Static Method to query Supabase for users matching a name query."""
        try:
            from supabaseClient import supabase
            res = supabase.table("users").select("user_id, name, monthly_income").ilike("name", f"%{name_query.strip()}%").execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"Error finding user: {e}")
            return []
