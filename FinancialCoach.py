class FinancialCoach:
    def __init__(self, recommendation="No recommendations yet.", spendingPattern="No spending data available."):
        self.recommendation = str(recommendation)
        self.spendingPattern = str(spendingPattern)

    def analyzeSpending(self):
        return self.spendingPattern

    def giveSuggestion(self):
        return self.recommendation

    def predictCashFlow(self, monthlyIncome=0.0, currentExpenses=0.0):
        try:
            income = float(monthlyIncome)
            expenses = float(currentExpenses)
            net_flow = income - expenses
            
            if net_flow > 0:
                return f"Projected Net Surplus: ₱{net_flow:,.2f} remaining at current spending rates."
            elif net_flow < 0:
                return f"Projected Net Deficit: You are projected to overspend by ₱{abs(net_flow):,.2f}."
            else:
                return "Projected Cash Flow: Breaking even."
        except (ValueError, TypeError):
            return self.spendingPattern