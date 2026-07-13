from bank import Account
from bank import account
acc = Account("sofoniyas", "5000")
acc.deposit(1000)
acc.withdraw(500)
acc.statement()
print("Current balance:", acc.balance)
