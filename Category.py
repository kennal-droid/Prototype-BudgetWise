class Category:
    def __init__(self, categoryID, categoryName, spendLimit=0.0):
        self.categoryID = categoryID
        self.categoryName = categoryName
        self.spendLimit = float(spendLimit)

    def setLimit(self, newLimit):
        self.spendLimit = float(newLimit)

    def checkLimit(self, currentSpending):
        currentSpending = float(currentSpending)
        if currentSpending > self.spendLimit:
            return f"⚠️ Alert: Spending in {self.categoryName} has exceeded your limit of ₱{self.spendLimit:,.2f}!"
        return f"✅ Spending in {self.categoryName} is within your limit."