import sqlite3

conn = sqlite3.connect('transactions.db')
c = conn.cursor()


class Person:
    def __init__(self,tdate, ttime, ref, name, address, ttype, remarks, debit, credit):
        self.tdate = tdate
        self.ttime = ttime
        self.ref = ref
        self.name = name
        self.address = address
        self.remarks = remarks
        self.debit = debit
        self.credit = credit
        self.ttype = ttype
    c.execute("""CREATE TABLE IF NOT EXISTS statements(
                    date DATE,
                    time TIME,
                    ref INT, 
                    name TEXT,
                    address CHAR,
                    type TEXT,
                    remarks TEXT,
                    debit REAL,
                    credit REAL)""")

    def add(self):
        with conn:

            c.execute("INSERT INTO statements VALUES(:date, :time, :ref, :name, :address, :ttype, :remarks, :debit, :credit)",
                      { 'date':self.tdate,'time':self.ttime ,'ref': self.ref, 'name': self.name, 'address': self.address, 'ttype': self.ttype,
                       'remarks': self.remarks, 'debit': self.debit, 'credit': self.credit})


class Customer:
    def __init__(self, name, address, contact):
        self.name = name
        self.address = address
        self.contact = contact
    c.execute("""CREATE TABLE IF NOT EXISTS customers(
                    name CHAR,
                    address CHAR,
                    contact INT)""")

    def add(self):
        with conn:
            c.execute("INSERT INTO customers VALUES(:name, :address, :contact)",{'name':self.name, 'address':self.address, 'contact':self.contact})


class Dealer:
    def __init__(self, name, address, contact):
        self.name = name
        self.address = address
        self.contact = contact

    c.execute("""CREATE TABLE IF NOT EXISTS dealers(
                    name CHAR,
                    address CHAR,
                    contact INT)""")

    def add(self):
        with conn:
            c.execute("INSERT INTO dealers VALUES(:name, :address, :contact)"
            ,{'name':self.name, 'address':self.address, 'contact':self.contact})

def delete_transaction(ref, name):
    with conn:
        c.execute("DELETE FROM statements WHERE ref= :ref AND name =:name", {'name':name, 'ref':ref})


def delete_someone(name, address, type):
    if type =='Customer':
        with conn:
            c.execute("DELETE FROM customers WHERE name=:name AND address =:address",{'name':name,'address':address})
    elif type=='Dealer':
        with conn:
            c.execute("DELETE FROM dealers WHERE name=:name AND address =:address",{'name':name,'address':address})


def find(name):
    c.execute("SELECT * FROM statements WHERE name =:name", {'name': name})
    return c.fetchall()


def get_all():
    c.execute("SELECT date, time, ref, name, type, remarks, debit, credit FROM statements order by date")
    all = c.fetchall()
    sorted = [all[i] for i in reversed(range(len(all)))]
    return sorted


def get_all_for(name,address, type):
    c.execute("SELECT date, time, ref, name,remarks, debit, credit FROM statements WHERE name =:name AND address=:address AND type=:type order by name", {'name':name, 'type':type,'address':address})
    a = c.fetchall()
    sorted = [a[i] for i in reversed(range(len(a)))]
    return sorted


def evaluate_this(name):
    all_debit = c.execute("SELECT debit FROM statements WHERE name = :name",{'name': name}).fetchall()
    all_credit = c.execute("SELECT credit FROM statements WHERE name = :name",{'name': name}).fetchall()

    d_sum = 0
    c_sum = 0

    for i in all_debit:
        d_sum += i[0]
    for j in all_credit:
        c_sum += j[0]
    return d_sum-c_sum


def get_all_names():
    all = c.execute("SELECT name FROM statements").fetchall()
    x = [i[0] for i in all]

    from_c = c.execute('SELECT name FROM customers').fetchall()
    cx = [i[0] for i in from_c]

    from_d = c.execute('SELECT name FROM dealers').fetchall()
    dx = [i[0] for i in from_d]

    return list(set(x+cx+dx))


def debit_credit():
    debit = c.execute("SELECT debit FROM statements WHERE type='Customer'").fetchall()
    credit = c.execute("SELECT credit FROM statements WHERE type='Dealer'").fetchall()

    sold = 0
    bought=0

    for d in debit:
        sold += d[0]
    for cr in credit:
        bought += cr[0]
    return [sold, bought]


def all_customers_dealers_with_address(sm):
    result =c.execute('SELECT name, address FROM statements WHERE type=:x order by name', {'x': sm}).fetchall()
    alla = []
    allc = []
    all_c = []
    if sm=='Customer':
        all_c = c.execute('SELECT name,address FROM customers order by name').fetchall()
        alla = [result[i] for i in range(len(result))]
        allc = [all_c[i] for i in range(len(all_c))]
    elif sm=='Dealer':
        all_c = c.execute('SELECT name,address FROM dealers order by name').fetchall()
        alla = [result[i] for i in range(len(result))]
        allc = [all_c[i] for i in range(len(all_c))]
    return sorted(list(set(alla+allc)))

def all_dealers_customers(type):
    x = all_customers_dealers_with_address(type)
    return [i[0] for i in x]
    


def evaluate(this,loc, that):

    all_debit = c.execute('SELECT debit FROM statements WHERE name=:this AND address=:loc AND type=:that',{'this':this, 'that':that,'loc':loc}).fetchall()
    all_credit = c.execute('SELECT credit FROM statements WHERE name=:this AND address=:loc AND type=:that',{'this':this, 'that':that,'loc':loc}).fetchall()
    address = c.execute('SELECT address FROM statements WHERE name=:this AND address=:loc AND type=:that',{'this':this, 'that':that,'loc':loc}).fetchone()
    debit = [all_debit[i][0] for i in range(len(all_debit))]
    credit = [all_credit[i][0] for i in range(len(all_credit))]
    debit = sum(debit)
    credit = sum(credit)
    if address==None:
        if that=='Customer':
            addr=c.execute('SELECT address FROM customers WHERE name=:this',{'this':this}).fetchone()
        else:
            addr=c.execute('SELECT address FROM dealers WHERE name=:this',{'this':this}).fetchone()
        return addr[0], 'NA','NA'
    else:
        return address, debit, credit


def receivables_payables(who):
    all_d = c.execute("SELECT debit FROM statements WHERE type=:this",{'this':who}).fetchall()
    all_c = c.execute("SELECT credit FROM statements WHERE type=:this",{'this':who}).fetchall()

    debits =[i[0] for i in all_d]
    credits = [i[0] for i in all_c]

    debits = sum(debits)
    credits = sum(credits)

    if who == 'Dealer':
        return credits-debits
    elif who == 'Customer':
        return debits-credits

def details(name,address, type):
    if type =='Customer':
        ans =c.execute('SELECT contact FROM customers WHERE name=:name AND address=:address',{'name':name,'address':address}).fetchone()
    elif type=='Dealer':
        ans =c.execute('SELECT contact FROM dealers WHERE name=:name AND address=:address',{'name':name,'address':address}).fetchone()
    return ans[0]

def gimme_address(someone):
    try:
        try:
            cus =c.execute('SELECT address FROM customers WHERE name=:name',{'name':someone}).fetchone()
            return cus[0]
        except:
            deal =c.execute('SELECT address FROM dealers WHERE name=:name',{'name':someone}).fetchone()
            return deal[0]
    except:
        return ''