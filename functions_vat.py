#--------------For VAT and Stocks----------------#

import sqlite3
from datetime import date

conn = sqlite3.connect('stock&vat.db')
c = conn.cursor()


# ------- increased marked price percent from  cost price----------#
increased_mp = 0.2
#----------------profit percent on VAT sale-------------#
profit = 0.02


def get_quantity(product):
    """Returns how many certain products are left in stock."""
    try:
        c.execute('select quantity from stocks where product=:product',{'product':product})
        return c.fetchone()[0]
    except:
        return 0

def get_rate(product):
    """Returns the vat purchase rate from stocks"""
    try:
        c.execute('select rate from stocks where product=:product',{'product':product})
        return round(c.fetchone()[0],2)
    except:
        return 0

def get_actual_rate(product):
    """Returns the actual purchase rate from stocks"""
    try:
        c.execute('select actual_rate from stocks where product=:product',{'product':product})
        return round(c.fetchone()[0],2)
    except:
        return 0

def delete_from_stocks(product):
    with conn:
        c.execute('delete from stocks where product=:name',{'name':product})

def all_stocks():
    """Shows all products stocked."""
    alls = c.execute('select * from stocks order by product').fetchall()
    return [i[0] for i in alls]

def all_stocks_detail():
    """Shows all info about the stocked items."""
    all = c.execute('select * from stocks order by product').fetchall()
    return all

def stock_value():
    info = c.execute('select * from stocks').fetchall()
    amts = [float(i[2])*float(i[1]) for i in info]
    return round(sum(amts),2)

def all_sales():
    """shows all the details stored in sales database"""
    all = c.execute('select * from VATsales order by date').fetchall()
    return all

def all_purchases():
    """shows all the details stored in purchases database"""
    all = c.execute('select * from VATpurchases order by date').fetchall()
    return all

def details_on_invoice(ref, date, name, ttype):
    if ttype=='Dealer':
        all = c.execute("select product, quantity, rate, actual_rate from VATpurchases where reference=:ref and date=:date and dealer=:dealer",
                {'ref':ref, 'date':date,'dealer':name}).fetchall()
        return all
    elif ttype=='Customer':
        all = c.execute("select product, quantity, rate from VATsales where reference=:ref and date=:date and customer=:customer",
                {'ref':ref, 'date':date,'customer':name}).fetchall()
        return all

def invoice_details(ttype):
    details = c.execute('select ref, date, name, remarks, amount, vat from invoice where type=:type order by date desc',{'type':ttype}).fetchall()
    return details


def total_amount(ref, name, type):
    if type =='Dealer':
        details = c.execute('select rate, quantity from VATpurchases where reference=:ref and dealer=:name',{'ref':ref,'name':name}).fetchall()
        amt = [float(i[0])*float(i[1]) for i in details]
        return round(sum(amt),2)
    else:
        details = c.execute('select rate, quantity from VATsales where reference=:ref and customer=:name',{'ref':ref,'name':name}).fetchall()
        amt = [float(i[0])*float(i[1]) for i in details]
        return round(sum(amt),2)

class Stocks():
    def __init__(self, product,  quantity, rate,actual_rate):
        self.product = product
        self.quantity = int(quantity)
        self.rate = rate
        self.actual_rate = actual_rate
    c.execute("""
                create table if not exists stocks(
                product text primary key not null,
                quantity int not null,
                rate char not null,
                actual_rate char not null)
                """)

    def add_stock(self):
        """Adds the instantiated product to stock."""
        current_quantity = int(get_quantity(self.product))
        
        if current_quantity == 0 and self.product not in all_stocks():
            with conn:
                c.execute('insert into stocks values(:product,:quantity,:rate,:actual_rate)',
                          {'product':self.product, 'quantity':self.quantity,'rate':self.rate,'actual_rate':self.actual_rate})
        else:
            with conn:
                c.execute("update stocks set quantity=:new_quantity where product=:product",
                          {'new_quantity':current_quantity+self.quantity,'product':self.product})
                
    def remove_stock(self):
        """Removes the instantiated product from stock."""
        current_quantity = get_quantity(self.product)
        if (current_quantity- self.quantity <0):
            raise Exception('StockedQuantityInsufficient')
        else:
            with conn:
                c.execute("update stocks set quantity=:new_quantity where product=:product",
                        {'new_quantity':current_quantity-self.quantity,'product':self.product})

def amount_purchased():
    all = c.execute('select quantity, rate from VATpurchases').fetchall()
    multiplied = [i[0]* i[1] for i in all]
    return round(sum(multiplied),2)

def amount_sold():
    all = c.execute('select quantity, rate from VATsales').fetchall()
    multiplied = [i[0]* i[1] for i in all]
    return round(sum(multiplied),2)

class StocksPurchases():
    def __init__(self,reference,date:str,dealer,product, quantity, rate, actual_rate):
        self.product = product
        self.quantity = quantity
        self.rate = rate
        self.actual_rate = actual_rate
        self.date = date
        self.reference = reference
        self.dealer = dealer
        self.remarks = predict_remarks(self.product)

    c.execute("""
            create table if not exists VATpurchases(
                reference char,
                date char,
                dealer text,
                product text not null,
                quantity int,
                rate float,
                actual_rate float)
            """)
    def buy(self):
        """Adds the transaction to the database and maintains the stock."""
        with conn:
            c.execute("insert into VATpurchases values(:reference,:date,:dealer, :product,:quantity, :rate, :actual_rate)",
            {'product':self.product,'rate':self.rate,'actual_rate':self.actual_rate,
             'quantity':self.quantity,'date':self.date, 'reference':self.reference,'dealer':self.dealer})

        Stocks(self.product, self.quantity, self.rate, float(self.actual_rate)*(1+increased_mp)).add_stock()
        create_invoice()

class StocksSales():
    def __init__(self,reference,date:str,customer:str, product, quantity):
        self.product = product
        self.reference = reference
        self.quantity = quantity
        rate = c.execute('select rate from stocks where product=:product',{'product':self.product}).fetchone()[0]
        self.rate = round(float(rate)+profit*float(rate),2)
        self.date = date
        self.customer = customer
        self.remarks = predict_remarks(self.product)

    c.execute("""
            create table if not exists VATsales(
                reference char,
                date char,
                customer text,
                product text not null,
                quantity int,
                rate float)
    """)
    def sell(self):
        """
        Adds the transaction to the database and maintains stock."""
        try:
            Stocks(self.product, self.quantity, get_rate(self.product), get_actual_rate(self.product)).remove_stock()      

            with conn:
                c.execute("insert into VATsales values(:reference,:date,:customer, :product,:quantity,:rate)", {'product':self.product,'quantity':self.quantity,
                'rate':self.rate, 'date':self.date,'reference':self.reference,'customer':self.customer})
            create_invoice()
               
        except:
            raise Exception('StockedQuantityInsufficient')

        
def delete_vat_transactions(ref, name, ttype):
    """Delete transactions from vat database based on reference no, name and type"""
    if ttype =='Sales':
        info = c.execute("select product, quantity from VATsales where reference=:ref and customer=:name",{'ref':ref,'name':name}).fetchall()
        for items in info:
            (issued_product,issued_quantity) = items
            Stocks(issued_product, issued_quantity, get_rate(issued_product), get_actual_rate(issued_product)).add_stock()

        with conn:
            c.execute("DELETE FROM VATsales WHERE reference=:ref and customer=:name",{'name':name,'ref':ref})

    elif ttype=='Purchases':
        info = c.execute("select product, quantity from VATpurchases where reference=:ref and dealer=:name",{'ref':ref,'name':name}).fetchall()
        for items in info:
            (issued_product, issued_quantity) = items
            Stocks(issued_product, issued_quantity ,get_rate(issued_product), get_actual_rate(issued_product)).remove_stock()
        with conn:
            c.execute("DELETE FROM VATpurchases WHERE reference=:ref and dealer=:name",{'name':name,'ref':ref})

class Invoice():
    def __init__(self, ref, date, name, remarks,ttype, amount):
        self.ref = ref
        self.date = date
        self.name = name
        self.remarks = remarks 
        self.amount = amount
        self.vat = round(0.13*float(self.amount),2)
        self.ttype = ttype

    c.execute("""
                create table if not exists invoice(
                    ref char not null,
                    date char not null,
                    name char not null,
                    remarks char,
                    type char,
                    amount char,
                    vat char
                )""")
    def add_invoice(self):
        with conn:
            c.execute('insert into invoice values(:ref, :date, :name, :remarks,:type,:amount,:vat)',{
                'ref':self.ref,
                'date':self.date,
                'name':self.name,
                'remarks':self.remarks,
                'amount':self.amount,
                'vat':self.vat,
                'type':self.ttype
            })

def create_invoice():
    with conn:
        c.execute("""delete from invoice""")
        # ------for purchases---------

    all_info = c.execute('select reference, date, dealer from VATpurchases').fetchall()
    all_info = list(set(all_info))
    
    for i in range(len(all_info)):
        ref = all_info[i][0]
        date = all_info[i][1]
        dealer = all_info[i][2]

        details = c.execute('select product, quantity, rate from VATpurchases where reference=:ref and date=:date and dealer=:dealer',
                                    {'ref':ref,'date':date,'dealer':dealer}).fetchall()
        products =[i[0] for i in details]

        remarks = predict_remarks(products)

        amount = [float(i[1])*float(i[2]) for i in details]
        amount = round(sum(amount),2)
        ttype='Purchases'
        Invoice(ref, date, dealer, remarks, ttype, amount).add_invoice()

    # ---------for sales-------
    all_infos = c.execute('select reference, date, customer from VATsales').fetchall()
    all_infos = list(set(all_infos))
    
    for i in range(len(all_infos)):
        ref = all_infos[i][0]
        date = all_infos[i][1]
        customer = all_infos[i][2]

        details = c.execute('select product, quantity, rate from VATsales where reference=:ref and date=:date and customer=:customer',
                                    {'ref':ref,'date':date,'customer':customer}).fetchall()
        remarks = predict_remarks(details[0][0])

        amount = [float(i[1])*float(i[2]) for i in details]
        amount = round(sum(amount),2)
        ttype='Sales'
        Invoice(ref, date, customer, remarks, ttype, amount).add_invoice()


def delete_invoice(ref, name, ttype):
    with conn:
        c.execute('delete from invoice where ref=:ref and name=:name and type=:type',{'ref':ref,'name':name,'type':ttype})


def predict_remarks(products):
    
    words = []
    for i in products:
        words.extend(i.split(' '))
    dicts={'Furnitures':['CHAIR','DINING','SHOWCASE','BED','SOFA','LOW-BED','DARAJ','PALANG','DRESSING','TABLE','CORNER','SOFA'],
            'Electronics':['FRIDGE','VACUUM','OVEN','MIXER','GRINDER','COOKER','FRYER','ELECTRIC','JUG','JAR','BALTRA','LED','BULB','HEATER',
                            'FOSTER','INDUCTION'],
            'Hardware':['ROD', 'SS','PIPE','PLY'],
            'Furnishing Items':['PARDA','BEDSHEET','B/S','JHUL','HANGER','SHELF','CURTAIN','PILLOW','COVER','MOP', 'MAT','CARPET'],
            'Plastic Items':['CHAIR','TABLE','TBL/S','TBL/R','LM','BAGMATI','CH','PLASTIC','MAT','BABY']
            }
    predictions = []
    for j in range(len(words)):
        ans=''
        for i in words:
            if i in dicts['Furnishing Items']:
                ans= 'Furnishing Items'
            elif i in dicts['Electronics']:
                ans= 'Electronics'
            elif i in dicts['Hardware']:
                ans= 'Hardware'
            elif i in dicts['Furnitures']:
                ans= 'Furnitures'
            elif i in dicts['Plastic Items']:
                ans= 'Plastic Items'
            else:
                ans= 'Unknown Item'
            predictions.append(ans)    
    counter = 0
    predicted = predictions[0]
    unknown = predictions.count('Unknown Item')
    try:
        predictions.remove('Unknown Item')
    except:
        None
    
    for item in predictions:
        curr = predictions.count(item)
        if curr>counter:
            counter = curr
            predicted = item
    if counter+100>unknown:
        return predicted
    else:
        return 'Unknown Item'