class UserBudget:
    def __init__(self, budgetID, monthlyLimit, currentSpending=0.0, remainingBudget=0.0):
        self.budgetID = budgetID
        self.monthlyLimit = float(monthlyLimit)
        self.currentSpending = float(currentSpending)
        self.remainingBudget = float(remainingBudget)

    def calculateRemaining(self):
        self.remainingBudget = self.monthlyLimit - self.currentSpending
        return self.remainingBudget

    def checkBudgetStatus(self):
        if self.currentSpending > self.monthlyLimit:
            return "Over Budget"
        elif self.currentSpending >= (self.monthlyLimit * 0.8):
            return "Warning: 80% of Budget Reached"
        else:
            return "Within Budget"

    def sendAlert(self):
        if self.currentSpending > self.monthlyLimit:
            return "Alert: You are over budget!"
        elif self.currentSpending >= (self.monthlyLimit * 0.8):
            return "Alert: You have reached 80% of your budget limit!"
        else:
            return "Alert: You are within budget!!"