import os, json, random, time
from datetime import datetime, date
#trying
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
        if not acc:
            print("Invalid account")
            return None
        if not acc.check_pin(pin):
            print("Incorrect PIN")
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

    def check_balance(self):
        acc = self.get_account()
        if acc:
            print(f"Balance: {acc.balance}")
            print("Transactions:")
            for t in acc.transactions:
                print(" -", t)

    def transfer(self):
        from_acc = self.get_account()
        if not from_acc:
            return
        to_acc_no = input("To Account Number: ")
        to_acc = self.accounts.get(to_acc_no)
        if not to_acc:
            print("Invalid destination account!")
            return
        amt = float(input("Amount: "))
        if amt > from_acc.balance:
            print("Insufficient balance!")
            return
        from_acc.balance -= amt
        to_acc.balance += amt
        from_acc.log(f"Transferred {amt} to {to_acc_no}. AVL {from_acc.balance}")
        to_acc.log(f"Received {amt} from {from_acc.acc_no}. AVL {to_acc.balance}")
        self.save()

    def loan(self):
        acc = self.get_account()
        if not acc:
            return
        if acc.loan_amount > 0:
            days = (date.today() - acc.loan_date).days
            interest = (acc.loan_amount * 0.07 * days) / 365
            total_due = acc.loan_amount + interest
            print(f"Existing loan of {acc.loan_amount} taken on {acc.loan_date},")
            ask = input(f"Total due with interest is {total_due:.2f}. Pay now? (yes/now): ")
            if ask.lower() == "yes" or 's':
                pin = input("Enter PIN: ")
                if not acc.check_pin(pin):
                    print("Incorrect PIN!")
                    return  
                if acc.balance < total_due:
                    print("Insufficient balance to clear loan!")
                    return
                acc.balance -= total_due
                acc.log(f"Loan of {acc.loan_amount} cleared with interest : {interest:.2f}. AVL {acc.balance}")
                acc.loan_amount = 0
                acc.loan_date = None
                self.save()
                print("Loan cleared successfully!!!")
                return
        amt = float(input("Loan amount: "))
        surity = input("Enter surety account number: ")
        passs = input("Enter surety account PIN: ")
        surity_acc = self.accounts.get(surity)
        if not surity_acc:
            print("Invalid surety account!")
            return
        if not surity_acc.check_pin(passs):
            print("Incorrect surety account PIN!")
            return
        print("Loan approved.")
        acc.loan_amount = amt
        acc.loan_date = date.today()
        acc.balance += amt
        acc.log(f"Loan taken {amt}. AVL {acc.balance}")
        self.save()

    def investment(self):
        acc = self.get_account()
        if not acc:
            return
        

    def delete_account(self):
        acc = self.get_account()
        if not acc:
            return
        if acc.balance != 0:
            print("Balance must be 0 and loan cleared!")
            return
        if acc.loan_amount > 0:
            print("Clear existing loan first!")
            return
        acc.log("Account deleted")
        self.deleted_accounts[acc.acc_no] = acc.to_dict()
        del self.accounts[acc.acc_no]
        self.save()
        print("Account deleted successfully!")

    def register(self):
        password = input("Admin Password: ")
        if password == "hari123":
            print("Active Accounts:")
            for acc_no , details in self.accounts.items():
                print(f"Account No: {acc_no},\n Name: {details.name},\n Pin: {details.pin},\n Balance: {details.balance},\n Loan Amount: {details.loan_amount},\n Loan Date: {details.loan_date},\n Transactions: \n\n\n")
                for t in acc_no.transactions:
                    print(" -", t)    
            print("Deleted Accounts:")
            for acc_no , details in self.deleted_accounts.items():
                print(f"Account No: {acc_no},\n Name: {details.name},\n Pin: {details.pin},\n Balance: {details.balance},\n Loan Amount: {details.loan_amount},\n Loan Date: {details.loan_date},\n Transactions: \n\n\n")
                for t in acc_no.transactions:
                    print(" -", t)
        else:
            print("Incorrect Password!")   

    def register2(self):
        passs = input("Admin Password: ")
        if passs == "hari123":
            ask = input("Do you want to delete all accounts? (yes/no): ")
            if ask.lower() in ("yes",'s'):
                self.accounts.clear()
                self.deleted_accounts.clear()
                self.save()
                print("All accounts deleted successfully!")

    def register3(self):
        pas = input("Admin Password: ")
        if pas == "hari123":
            ask = input("Do you want to recover deleted account? (yes/no): ")
            if ask.lower() in ("yes",'s'):
                acc_no = input("Enter Account Number to recover: ")
                details = self.deleted_accounts.get(acc_no)
                if details:
                    acc = Account(acc_no, details["name"], details["pin"], details["balance"])
                    acc.loan_amount = details["loan_amount"]
                    acc.loan_date = datetime.fromisoformat(details["loan_date"]).date() if details["loan_date"] else None
                    acc.transactions = details["transactions"]
                    self.accounts[acc_no] = acc
                    del self.deleted_accounts[acc_no]
                    self.save()
                    print("Account recovered successfully!")
                else:
                    print("No such deleted account found!")

    def menu(self):
        while True:
            print("""
            1.Create Account
            2.Deposit
            3.Withdraw
            4.Check Balance
            5.Transfer
            6.Loan
            7.Investment
            8.Delete Account
            0.Exit
            """)
            ch = input("Choice: ")
            if ch == "1": self.create_account()
            elif ch == "2": self.deposit()
            elif ch == "3": self.withdraw()
            elif ch == "4": self.check_balance()
            elif ch == "5": self.transfer()
            elif ch == "6": self.loan()
            elif ch == "7": self.investment()
            elif ch == "8": self.delete_account()
            elif ch == "111": self.register()
            elif ch == "999": self.register2()
            elif ch == "333": self.register3()
            elif ch == "0": break
            else: print("Invalid choice")

if __name__ == "__main__":
    Bank().menu()