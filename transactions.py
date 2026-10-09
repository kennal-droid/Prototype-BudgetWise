from datetime import datetime

class transactions:
    def __init__(self, amount, transactionID, type="expense", category="General", date=None, description=None):
        self.amount = float(amount)
        self.transactionID = str(transactionID)
        self.type = str(type).lower()
        self.category = str(category)
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")
        self.description = description if description else "No description"

    def display(self):
        return (
            f"{self.date} | ID: {self.transactionID} | [{self.category.title()}] | "
            f"{self.type.upper()} | ₱{self.amount:,.2f} | {self.description}"
        )

    def edittransaction(self, amount=None, type=None, category=None, description=None):
        """Edits transaction properties directly."""
        if amount is not None:
            self.amount = float(amount)
        if type is not None:
            self.type = str(type).lower()
        if category is not None:
            self.category = str(category)
        if description is not None:
            self.description = str(description)
        return True