# python3
"""
    generate a text file, which contains transactions for the account project
    The transactions are single lines consisting of
        an account number - taken out of an internal list
        a date  - generated randomly in a sortable format: yyyy-mm-dd
        an amount - a decimal number like 20.55, 12345.00, -250.00
        a text - this is some random text from the cicero file, limited to, say, 40 characters
"""

import os, os.path
import random
import datetime as DT
import math

path = 'data'
client_file_hdr = """# Clients for the PYWS Account project\n
# The names of clients start in column 1
# The account numbers start in column 4, there may be more than one account per client
# The account number is followed by an initial value for the account\n\n"""

transaction_file_hdr = """# Transactions for the PYWS Account project\n
# Each line defines one transaction
# The first column is the date, the second column is the account number
# Fhe third column is the amount (positive or negative)
# Following the amount there is a text field, which describes the transaction\n\n"""

def main():
    #test_set = ('A', 5, 200)
    test_set = ('B', 20, 999)
    set_id, nbr_clnt, nbr_tx = test_set

    accounts = build_clients(nbr_clnt, 'set{}-clients-({}).txt'.format(set_id, nbr_clnt))
    build_transactions(accounts, nbr_tx, "set{}-transactions-({})".format(set_id, nbr_tx))


def build_clients(number_of_clients, fname):
    gen_names = generate_edited_names()
    gen_acct = generate_acct_numbers()
    gen_amount = generate_amounts()
    account_nbrs = []

    filename = os.path.join(path, fname)
    with open(filename, mode='w', encoding='utf-8') as fo:
        fo.write(client_file_hdr)
        for x in range(number_of_clients):
            surname, firstname = next(gen_names)
            fo.write("{}, {}\n".format(surname, firstname))  # col=1 :  name of the client
            multi_account = random.random()
            for chance in (1.0, 0.3, 0.15):
                if chance < multi_account:
                    break
                acct_no = next(gen_acct)
                amt = next(gen_amount)
                initial = abs(amt)   # initial amount always positive
                fo.write("    {}  {:9.2f}\n".format(acct_no, initial)) # col=4: acct_no + init
                account_nbrs.append(acct_no)

    return account_nbrs

def build_transactions(accounts, number_of_transactions, fname):
    gen_acct = generate_imbalanced(accounts)
    gen_dates = generate_dates((2015,1,1), (2015,12,31))
    gen_amounts =generate_amounts()
    gen_text =generate_text()

    filename = os.path.join(path, fname)
    with open(filename, mode='w', encoding='utf-8') as fo:
        fo.write(transaction_file_hdr)
        for x in range(number_of_transactions):
            date = next(gen_dates)
            acct = next(gen_acct)
            amount = next(gen_amounts)
            text = next(gen_text)
            fo.write("{}  {}  {:7.2f}  {}\n".format(date, acct, amount, text))


# =============================================================================================

def generate_dates(fromdate, todate):
    # dates are passes as tuples of (y,m,d)
    y,m,d = fromdate
    fromdate = DT.date(y, m, d)
    y,m,d = todate
    todate = DT.date(y, m, d)
    range_from = fromdate.toordinal()
    range_to = todate.toordinal()
    while True:
        ordinal = random.randint(range_from, range_to+1)
        date_str = DT.date.fromordinal(ordinal).isoformat()
        yield date_str

def generate_amounts():
    while True:
        base = 1 + 5 * random.random()
        probe = base*base*base*base
        if probe < 5.0:
            continue    # no amounts < 5
        if probe < 800 and random.random() < 0.9:
            probe = - probe   # smaller amounts are mostly negative
        yield probe

def generate_text():
    text_list = []
    with open("data\\cicero.txt") as fi:
        for line in fi:
            tup = line.strip().split()
            if len(tup) < 8:
                continue
            text = ' '.join(tup[:8])
            text_list.append(text)

    while True:
        random.shuffle(text_list)
        for text in text_list:
            yield text

def generate_acct_numbers():
    acct_str = "{:04d}-{:04d}-{:02d}"
    R = random.randint
    old_acct = set()
    while True:
        acct_no = acct_str.format(R(1000, 4999), R(1, 9999), R(0,99))
        if acct_no in old_acct:
            continue  # avoid duplicates
        yield acct_no
        old_acct.add(acct_no)

def generate_imbalanced(list):
    imba_list = []
    for value in list:
        for x in range(random.randint(2,9)):
            imba_list.append(value)
    # now, some account numbers appear more often than others
    while True:
        yield random.choice(imba_list)

def generate_firstnames():
    for line in file_reader("data\\portuguese_firstnames.txt"):
        tup = line.split()
        if len(tup) < 2 or tup[1] not in ('m', 'f'):
            continue
        name, sex = tup[:2]
        name = name.capitalize()
        yield name, sex

def generate_surnames():
    for line in file_reader("data\\portuguese_surnames.txt"):
        if line[1] != line[1].upper():
            continue
        name = line.split()[0].capitalize()
        yield name
                    
def file_reader(fn):
    with open(fn, mode='r') as fi:
        for line in fi:
            line = line.rstrip()
            if len(line) < 5  or  line[0] == ' ':
                continue
            yield line            

def generate_raw_names():
    male = []
    female = []
    surname = []
    R = random.random
    for name, sex in generate_firstnames():
        if sex == 'f':
            female.append(name)
        else:
            male.append(name)

    for name in generate_surnames():
        surname.append(name)

    while True:
        firsttab = male if R() > 0.4 else female
        firstname = random.choice(firsttab)
        if R() < 0.2:
            firstname += ' '+ random.choice(firsttab)
        if R() < 0.05:
            firstname += ' '+ random.choice(firsttab)

        lastname = random.choice(surname)
        if R() < 0.3:
            lastname += ' '+ random.choice(surname)
        if R() < 0.1:
            lastname += ' '+ random.choice(surname)

        yield firstname, lastname
    # the output of the raw-names is manually edited into the 'portuguese_names.txt' file


def generate_edited_names():
    names = []
    with open("data\\portuguese_names.txt") as fi:
        for line in fi:
            line = line.rstrip()
            surname, firstname = line.split(', ')
            yield surname, firstname


def test():

    print("\nSurnames:\n")
    gener = generate_surnames()
    for x in range(20):
        print(next(gener))

    print("\nFirstnames:\n")
    gener = generate_firstnames()
    for x in range(20):
        f, l = next(gener)
        print(l+',', f)

    print("\nFull names (raw)\n")
    gener = generate_raw_names()
    for x in range(30):
        print(next(gener))

    print("\nFull names (edited)\n")
    gener = generate_edited_names()
    for x in range(20):
        print(next(gener))

    print("\nAccount numbers\n")
    gener = generate_acct_numbers()
    acct_list = []
    for x in range(5):
        acct_no = next(gener)
        acct_list.append(acct_no)
    for x in sorted(acct_list):
        print(x)

    print("\nAccount numbers (imbalanced)\n")
    gener = generate_imbalanced(acct_list)
    for x in range(20):
        print(next(gener))

    print("\nTransaction texts\n")
    gener = generate_text()
    for x in range(10):
        text = next(gener)
        print(len(text), text)

    print("\nTransaction dates\n")
    gener = generate_dates((2015,1,1), (2015,12,31))
    for x in range(10):
        print(next(gener))

    print("\nTransaction amounts\n")
    gener = generate_amounts()
    sum = 0
    for x in range(30):
        num = next(gener)
        print("{:7.2f}".format(num))
        sum += num
    print("sum of transactions: {:7.2f}".format(sum))

#
test()
#main()
