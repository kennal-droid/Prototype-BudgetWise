class SavingsGoal:
    def __init__(self, goalID, goalName, targetAmount, currentSavings=0.0):
        self.goalID = goalID
        self.goalName = goalName
        self.targetAmount = float(targetAmount)
        self.currentSavings = float(currentSavings)

    def addSavings(self, amount):
        amount = float(amount)
        if amount > 0:
            self.currentSavings += amount
            return True
        return False

    def calculateProgress(self):
        if self.targetAmount <= 0:
            return 0.0
        
        progress = (self.currentSavings / self.targetAmount) * 100
        return min(progress, 100.0)

    def checkGoalStatus(self):
        if self.currentSavings >= self.targetAmount:
            return "Goal Reached!!!"
        else:
            return "Goal has not been reached"