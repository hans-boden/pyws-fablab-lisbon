#python3
"""
    proposal for an account application
"""
import os, os.path

path = 'data'
client_file = 'setA-clients-(5).txt'
transact_file = 'setA-transactions-(200).txt'
output_file = 'account_list.txt'

class G():
    clients = []
    accounts = {}

def main():
    read_clients()
    read_transactions()

    fn = os.path.join(path, output_file)
    with open(fn, mode="w", encoding='utf-8') as fo:
        for print_line in report():
            fo.write(print_line+'\n')
    return


def report():
    tx_format  = "    {:10s}  {:50s}  {:9.2f}  {:9.2f}"
    bal_format = "    {:10s}  {:>50s}  {:9s}  {:9.2f}"

    for name, client in sorted(G.clients):
        yield 'Client: {}'.format(name)
        yield ''
        for account in client.accounts:

            yield 'Account number: {}'.format(account.account_no)
            balance = account.balance
            yield bal_format.format('', 'Start Balance', '', balance)
            yield ''
            for date, amount, text in sorted(account.transactions):
                balance += amount
                yield tx_format.format(date, text[:50], amount, balance)
            yield ''
            yield bal_format.format('', 'Final Balance', '', balance)
            yield ''

        yield '\f'  # form feed after the client

def read_transactions():
    fn = os.path.join(path, transact_file)
    for line in file_reader(fn):
        date, account_no, amount, text = line.split(None,3)
        account = G.accounts[account_no]
        account.add_transaction(date, amount, text)

def read_clients():
    fn = os.path.join(path, client_file)
    for line in file_reader(fn):
        if line[0] != ' ':   # line contains the client name
            name = line
            client = Client(name)
            G.clients.append((name, client))  # adding a tuple allows sorting
        else:   # following lines contain the accounts
            account_no, balance = line.split()
            account = Account(account_no, balance)
            client.add_account(account)
            G.accounts[account_no] = account

def file_reader(fn):
    with open(fn, mode='r', encoding='utf-8') as fi:
        for line in fi:
            line = line.split('#')[0].rstrip()
            if line == '':
                continue
            yield line

class Account():
    def __init__(self, account_no, balance):
        self.account_no = account_no
        self.balance = float(balance)
        self.transactions = []

    def add_transaction(self, date, amount, text):
        self.transactions.append((date, float(amount), text))

class Client():
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def add_account(self, account,):
        self.accounts.append(account)

main()
