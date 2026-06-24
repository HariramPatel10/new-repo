import os, json, random, time
from datetime import datetime, date

class Account:
    def __init__(self, acc_no, name, pin, balance):
        self.acc_no = acc_no
        self.name = name
        self.pin = pin
        self.balance = balance
        self.loan_amount = 0
        self.loan_date = None
        self.transactions = []
        self.log("Account created")

    def log(self, msg):
        self.transactions.append(
            f"{msg} at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def check_pin(self, pin):
        return self.pin == pin

    def to_dict(self):
        return {
            "name": self.name,
            "pin": self.pin,
            "balance": self.balance,
            "loan_amount": self.loan_amount,
            "loan_date": self.loan_date.isoformat() if self.loan_date else "",
            "transactions": self.transactions
        }


class Bank:
    DATA_FILE = "accounts.json"
    DELETE_FILE = "deleted_accounts.json"

    def __init__(self):
        self.accounts = {}
        self.deleted_accounts = {}
        self.load()

    def load(self):
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE) as f:
                data = json.load(f)
                for acc_no, d in data.items():
                    acc = Account(acc_no, d["name"], d["pin"], d["balance"])
                    acc.loan_amount = d["loan_amount"]
                    acc.loan_date = datetime.fromisoformat(d["loan_date"]).date() if d["loan_date"] else None
                    acc.transactions = d["transactions"]
                    self.accounts[acc_no] = acc

        if os.path.exists(self.DELETE_FILE):
            with open(self.DELETE_FILE) as f:
                self.deleted_accounts = json.load(f)

    def save(self):
        with open(self.DATA_FILE, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.accounts.items()}, f, indent=4)

        with open(self.DELETE_FILE, "w") as f:
            json.dump(self.deleted_accounts, f, indent=4)

    def generate_acc_no(self):
        while True:
            acc = str(random.randint(1000, 9999))
            if acc not in self.accounts:
                return acc

    def get_account(self):
        acc_no = input("Account Number: ")
        pin = input("PIN: ")
        acc = self.accounts.get(acc_no)
        if not acc or not acc.check_pin(pin):
            print("Invalid account or PIN!")
            return None
        return acc

    def create_account(self):
        name = input("Name: ")
        pin = input("Set PIN: ")
        bal = float(input("Initial deposit: "))
        acc_no = self.generate_acc_no()
        self.accounts[acc_no] = Account(acc_no, name, pin, bal)
        self.save()
        print("Account created:", acc_no)

    def deposit(self):
        acc = self.get_account()
        if acc:
            amt = float(input("Amount: "))
            acc.balance += amt
            acc.log(f"Deposited {amt}")
            self.save()

    def withdraw(self):
        acc = self.get_account()
        if acc:
            amt = float(input("Amount: "))
            if amt > acc.balance:
                print("Insufficient balance!")
                return
            acc.balance -= amt
            acc.log(f"Withdrawn {amt}")
            self.save()

    def loan(self):
        acc = self.get_account()
        if not acc:
            return

        if acc.loan_amount > 0:
            days = (date.today() - acc.loan_date).days
            interest = (acc.loan_amount * 0.07 * days) / 365
            print("Existing loan interest:", interest)
            return

        amt = float(input("Loan amount: "))
        acc.loan_amount = amt
        acc.loan_date = date.today()
        acc.balance += amt
        acc.log(f"Loan taken {amt}")
        self.save()

    def delete_account(self):
        acc = self.get_account()
        if not acc:
            return
        if acc.balance != 0 or acc.loan_amount > 0:
            print("Balance must be 0 and loan cleared!")
            return
        acc.log("Account deleted")
        self.deleted_accounts[acc.acc_no] = acc.to_dict()
        del self.accounts[acc.acc_no]
        self.save()
        print("Account deleted successfully!")

    def menu(self):
        while True:
            print("""
            1.Create Account
            2.Deposit
            3.Withdraw
            4.Loan
            5.Delete Account
            0.Exit
            """)
            ch = input("Choice: ")
            if ch == "1": self.create_account()
            elif ch == "2": self.deposit()
            elif ch == "3": self.withdraw()
            elif ch == "4": self.loan()
            elif ch == "5": self.delete_account()
            elif ch == "0": break
            else: print("Invalid choice")


if __name__ == "__main__":
    Bank().menu()
