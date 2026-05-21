from colorama import init, Fore, Back, Style
init()

class Bank:

    def __init__(self, name):
        self.name = name

    def transfer(self,account1,account2,amount):
        account1.withdraw(amount)
        account2.deposit(amount)


class BankAccount:

    def __init__(self, iban, bank:Bank, balance = 0):
        self.iban = iban
        self.balance = balance
        self.bank = bank

    def show_balance(self):
        if self.balance <= 500:
            print(Fore.YELLOW + f'Balance: {self.balance}₴' + Style.RESET_ALL)
        else:
            print(Fore.WHITE + f'Balance: {self.balance}₴' + Style.RESET_ALL)

    def deposit(self, amount):
        self.balance += amount
        print(f'account {self.iban}: + {amount} ₴')

    def withdraw(self, amount):
        if self.balance > amount:
            self.balance -= amount
            print(f'account {self.iban}: - {amount}₴')
        else:
            raise ValueError("⚠️Not enough money on balance")

    def transfer(self, amount, account):
        self.bank.transfer(self, account, amount)



privat_bank = Bank("Privat Bank")
mono_bank = Bank("Mono Bank")

mark_account = BankAccount(111, privat_bank, 1000)
john_account = BankAccount(222, mono_bank,500)

mark_account.show_balance()
# mark_account.deposit(500)

try:
    mark_account.transfer(1700,john_account)
except ValueError as ve:
    print(Fore.RED + f'{ve}' + Style.RESET_ALL)

mark_account.transfer(700, john_account)
john_account.show_balance()
mark_account.show_balance()