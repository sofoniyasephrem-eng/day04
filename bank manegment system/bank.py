import json
import os
import uuid
from typing import Dict, List, Optional

from account.nnn import BankAccount


class BankSystem:
    def __init__(self, file_path: str = "accounts.json") -> None:
        self.file_path = file_path
        self.accounts: Dict[str, BankAccount] = {}
        self._load_accounts()

    def _load_accounts(self) -> None:
        if not os.path.exists(self.file_path):
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.accounts = {
                account_id: BankAccount.from_dict(account_data)
                for account_id, account_data in data.items()
            }
        except (json.JSONDecodeError, OSError):
            self.accounts = {}

    def _save_accounts(self) -> None:
        directory = os.path.dirname(self.file_path) or "."
        os.makedirs(directory, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                {account_id: account.to_dict()
                 for account_id, account in self.accounts.items()},
                file,
                indent=2,
            )

    def create_account(self, holder_name: str, initial_deposit: float = 0.0) -> BankAccount:
        if not holder_name.strip():
            raise ValueError("Account holder name cannot be empty.")
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative.")

        account = BankAccount(
            account_number=f"ACC-{uuid.uuid4().hex[:8].upper()}",
            holder_name=holder_name.strip(),
            balance=float(initial_deposit),
        )
        self.accounts[account.account_number] = account
        self._save_accounts()
        return account

    def deposit(self, account_number: str, amount: float) -> bool:
        account = self.accounts.get(account_number)
        if not account or amount <= 0:
            return False
        account.deposit(amount)
        self._save_accounts()
        return True

    def withdraw(self, account_number: str, amount: float) -> bool:
        account = self.accounts.get(account_number)
        if not account or amount <= 0:
            return False
        success = account.withdraw(amount)
        if success:
            self._save_accounts()
        return success

    def get_balance(self, account_number: str) -> Optional[float]:
        account = self.accounts.get(account_number)
        if account is None:
            return None
        return account.balance

    def get_account(self, account_number: str) -> Optional[BankAccount]:
        return self.accounts.get(account_number)

    def list_accounts(self) -> List[BankAccount]:
        return list(self.accounts.values())


def _prompt_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def main() -> None:
    bank = BankSystem("accounts.json")
    print("Welcome to the Bank Management System")
    print("==================================")

    while True:
        print("\n1. Create account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Check balance")
        print("5. View all accounts")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Enter account holder name: ").strip()
            initial_deposit = _prompt_float("Enter initial deposit: ")
            account = bank.create_account(name, initial_deposit)
            print(
                f"Account created successfully. Account number: {account.account_number}")

        elif choice == "2":
            account_number = input("Enter account number: ").strip()
            amount = _prompt_float("Enter deposit amount: ")
            if bank.deposit(account_number, amount):
                print("Deposit successful.")
            else:
                print("Deposit failed. Please check the account number and amount.")

        elif choice == "3":
            account_number = input("Enter account number: ").strip()
            amount = _prompt_float("Enter withdrawal amount: ")
            if bank.withdraw(account_number, amount):
                print("Withdrawal successful.")
            else:
                print("Withdrawal failed. Insufficient funds or invalid account.")

        elif choice == "4":
            account_number = input("Enter account number: ").strip()
            balance = bank.get_balance(account_number)
            if balance is None:
                print("Account not found.")
            else:
                print(f"Current balance: {balance:.2f}")

        elif choice == "5":
            accounts = bank.list_accounts()
            if not accounts:
                print("No accounts found.")
            else:
                for account in accounts:
                    print(
                        f"{account.account_number} | {account.holder_name} | Balance: {account.balance:.2f}")

        elif choice == "6":
            print("Thank you for using the bank management system.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
