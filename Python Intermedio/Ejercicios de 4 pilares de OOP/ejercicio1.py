class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("You cannot deposit a negative amount")
        self.balance += amount

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("You cannot withdraw a negative amount")
        self.balance -= amount


class SavingsAccount(BankAccount):
    def __init__(self, balance, min_balance):
        super().__init__(balance)
        self.min_balance = min_balance

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("You cannot withdraw a negative amount")
        if self.balance - amount < self.min_balance:
            raise ValueError(
                "Withdrawal denied: balance would fall below the minimum required"
            )
        self.balance -= amount