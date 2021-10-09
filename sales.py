from tkinter import *
from typing import ValuesView
from functions import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from functions_vat import *
from tkinter import ttk
from nepali_datetime import date

# --------------Fonts--------------- #
huge_font = ('Comic Sans MS', 60, 'bold')
medium_font = ('Comic Sans MS', 49)
small_font = ('Comic Sans MS', 30)
tiny_font = ('Comic Sans MS', 20)
medium_lined = ('Imprint MT Shadow', 55, 'underline')
very_small = ('Comic Sans MS', 15)
tree_font = ('Georgia', 20)
dialog_font = ("Georgia", 40)
head_text = ('Lucida Calligraphy',40)
huge_tree =('Georgia',50)

back = '#9effcd'


class Sales(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        func_frame = Frame(self, height=200,padx=10, pady=10, bg=back)
        func_frame.pack(side=TOP, fill=X)
        func_frame.grid_columnconfigure(3, weight=2)

        head = Label(func_frame, text='Sales', font=medium_lined, bg=back, fg='dark blue')
        head.grid(row=1, column=1, columnspan=2)

        stocksb = Button(func_frame, relief=GROOVE, bd=4, text='Stocks', bg='silver', fg='brown', font=tiny_font,
                       height=1, width=10, command=lambda: controller.show_frame('StocksPage'))
        stocksb.grid(row=2, column=1, padx=5)

        purchasesb = Button(func_frame, relief=GROOVE, bd=4, text='Purchases', bg='red', fg='white', font=tiny_font, height=1,
                       width=10, command=lambda: controller.show_frame('Purchases'))
        purchasesb.grid(row=2, column=2)

        sold_amount = Label(func_frame, font=medium_font, bg='#52c433', fg='white', padx=25, pady=10,
                            relief=RIDGE, bd=5, width=10)
        sold_amount.grid(row=1, column=5, sticky=NE, padx=5)

        Label(func_frame, text='Sold:',fg='purple', font=head_text, bg=back).grid(row=1, column=4, sticky=NE, padx=5)

        sell_button = Button(func_frame, text='-Sell Goods', font=tiny_font, bg='#2930ff', fg='white', bd=4, relief=GROOVE,
                            width=10, command=lambda :get_details_sell())
        sell_button.grid(row=2, column=5,sticky=W, padx=4, pady=5)

        delete_button = Button(func_frame, text='Delete', font=tiny_font, bg='#2930ff', fg='white', bd=4, relief=GROOVE,
                             width=6, command=lambda:get_details_delete())
        delete_button.grid(row=2, column=5,padx=2, sticky=E, pady=5)

        def get_details_delete():
            bg='silver'
            delete_window = Toplevel(self, bg=bg, padx=10,pady=10)
            delete_window.title('Delete Sold Transactions')
            delete_window.geometry('600x300')

            Label(delete_window, text='Enter Transaction Details:', font=small_font,bg=bg).grid(row=1, column=1,columnspan=2, sticky='nsew')
            Label(delete_window, text='Reference No.', font=tiny_font,bg=bg).grid(row=2,column=1,sticky=NSEW)
            Label(delete_window, text='Name:', font=tiny_font,bg=bg).grid(row=3,column=1,sticky='nsew')

            reference = Entry(delete_window, font=tiny_font)
            name= Entry(delete_window, font=tiny_font)

            reference.grid(row=2, column=2, sticky='nsew')
            name.grid(row=3,column=2, sticky='nsew')

            delete_b = Button(delete_window,font=small_font, text='Delete',bg='orange',command=lambda:delete_sales(), width=2, height=1)
            delete_b.grid(row=5, column=2,sticky='nsew',padx=10, pady=10)

            def delete_sales():
                n = name.get().upper()
                ref = reference.get().upper()

                delete_vat_transactions(ref,n,'Sales')
                delete_invoice(ref, n, 'Sales')

                refresh_and_add()
                delete_window.destroy()

        def get_details_sell():
            bg='#aebefc'
            add_window=Toplevel(self, bg=bg, padx=10, pady=10)
            add_window.title('Sell Goods')

            Label(add_window, text='Enter Sales Details:', font=small_font,bg=bg).grid(row=1, column=1, columnspan=2,sticky='nw')

            Label(add_window, text='Reference No.', font=tiny_font,bg=bg).grid(row=2, column=1, sticky='nw')
            Label(add_window, text='Date:', font=tiny_font,bg=bg).grid(row=2,column=3,sticky='nw')
            Label(add_window, text='Customer:', font=tiny_font,bg=bg).grid(row=3,column=1,sticky='nw')

            Label(add_window,text='Product:', font=tiny_font,bg=bg).grid(row=4, column=1,sticky='nw')
            Label(add_window,text='Quantity:', font=tiny_font,bg=bg).grid(row=4, column=3,sticky='nw')

            tref = Entry(add_window, font=tiny_font)
            tdate = Entry(add_window, font=tiny_font)
            tdate.insert(0, date.today())


            n = StringVar()
            tcustomer = Combobox(add_window, width=19, textvariable=n, font=tree_font)
            tcustomer['values'] = all_dealers_customers('Customer')

            tref.grid(row=2, column=2,sticky='nw', padx=2, pady=2)
            tdate.grid(row=2, column=4,sticky='nw', padx=2, pady=2)
            tcustomer.grid(row=3, column=2,sticky='nw', padx=2, pady=2)

            item_frame = Frame(add_window, padx=2, pady=2)
            item_frame.grid(row=5, column=1, columnspan=4, sticky='nw')
            
            details = [tref, tdate, tcustomer]
            entries = []

            def add_entry():
                frame = Frame(item_frame)
                frame.pack()

                p = StringVar()
                product = Combobox(frame, textvariable=p, font=tree_font)
                product['values'] = all_stocks()
                quantity = Entry(frame, font=tiny_font)
                rate = Entry(frame, font=tiny_font)
                actual_rate = Entry(frame, font=tiny_font)

                var = [product, quantity]

                for j,i in enumerate(var):
                    i.grid(row=1, column=3**j, columnspan=2, padx=10)
                entries.append(var)

            increase = Button(add_window, text='+',command=add_entry, font=very_small, bg='white')
            increase.grid(row=4, column=5, sticky='nw')

            def iterate():
                info = []
                values = []
                for i in entries:
                    ans = []
                    for val in i:
                        ans.append(val.get().upper())
                    values.append(ans)

                for i in details:
                    info.append(i.get().upper())
                return (info,values)


            confirm_b = Button(add_window, text='Add',font=small_font,bg='#aeff2b', command=lambda :sell_stocks())
            confirm_b.grid(row=9,column=2,sticky='nsew',padx=10, pady=10)


            def sell_stocks():
                info, values = iterate()
                for items in values:

                    if "" not in info and "" not in items:
                        try:
                            StocksSales(info[0],info[1], info[2], items[0], items[1]).sell()
                        except:
                            messagebox.showerror(title='Error', message='Insufficient Product in Stock')
                    else:
                        messagebox.showerror(title='Error', message='Please fill all fields')
                add_window.destroy()
                refresh_and_add()

        def show_info(event):
            for selected_item in saless.selection():
                item = saless.item(selected_item)
                someone=item['values']

                date = someone[1]
                reference = someone[0]
                name = someone[2]
                 
                info_window = Toplevel(self)
                info_window.title('Invoice for '+name)
                info_window.geometry('1150x700')

                bg='#fdffc7'

                head_frame = Frame(info_window,bg=bg)
                head_frame.pack(fill=X)

                Label(head_frame, text='Date: '+str(date), font=small_font, bg=bg, fg='brown', bd=4).grid(row=1, column=1, columnspan=10,sticky='nw', padx=10, pady=10)
                Label(head_frame, text='Reference:'+str(reference), font=small_font, bg=bg, fg='brown').grid(row=3, sticky='nw', column=1, padx=10, pady=10)
                Label(head_frame, text='Customer:'+str(name), font=small_font,bg=bg, fg='brown').grid(row=4 ,column=1,sticky='nw', padx=10, pady=10)

                table_frame = Frame(info_window, bg='yellow', relief=GROOVE, bd=5)
                table_frame.pack(side=TOP, padx=10, pady=10, fill=BOTH, expand=True)

                stats =ttk.Treeview(table_frame, columns=(1,2,3), show='headings', style='Treeview')
                stats.pack(side=LEFT,fill=BOTH, expand=True)

                scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=stats.yview)
                stats.configure(yscroll=scrollbar.set)
                scrollbar.pack(side=RIGHT, fill=Y)
                headings = ['Product','Quantity', 'VAT Rate',]

                for h in headings:
                    stats.heading(headings.index(h)+1, text=h)
                    if h!='Product':
                        stats.column(headings.index(h)+1, minwidth=50, width=150)
                    else:
                        stats.column(headings.index(h)+1, minwidth=50, width=300)


                style = ttk.Style()
                style.theme_use('default')
                style.map('Treeview')
                style.configure('Treeview', font=tiny_font, rowheight=40)
                style.configure('Treeview.Heading', font=(tree_font))

                def refresh_add():

                    stats.delete(*stats.get_children())
                    transactions = details_on_invoice(reference, date, name, 'Customer')
                    for i in range(len(transactions)):
                        statements = transactions[i]
                        stats.insert('', index=i+1, values=statements)
                refresh_add()
    # ---------------------------------------Table -----------------------------------------#
# --------------------show info function-----------------#

        
        table_frame = Frame(self, bg='yellow', relief=GROOVE, bd=5)
        table_frame.pack(side=TOP, padx=10, pady=10, fill=BOTH, expand=True)

        saless =ttk.Treeview(table_frame, columns=(1,2,3,4,5,6), show='headings', style='Treeview')
        saless.pack(side=LEFT,fill=BOTH, expand=True)
        saless.bind('<<TreeviewSelect>>', show_info)


        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=saless.yview)
        saless.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        headings = ['Ref.No.','Date','Name','Remarks','Amount','VAT']
        for h in headings:
            saless.heading(headings.index(h)+1, text=h)
            if h in ['Amount','VAT','Ref.No.', 'Date']:
                saless.column(headings.index(h)+1, minwidth=50, width=125)
            else:
                saless.column(headings.index(h)+1, minwidth=50, width=220)

        style = ttk.Style()
        style.theme_use('default')
        style.map('Treeview')
        style.configure('Treeview', font=tiny_font, rowheight=40)
        style.configure('Treeview.Heading', font=(tree_font))

        def refresh_and_add():
            saless.delete(*saless.get_children())
            
            transactions = invoice_details('Sales')
            for i in range(len(transactions)):
                statements = transactions[i]
                saless.insert('', index=i, values=statements)
            sold = amount_sold()
            sold_amount.config(text='Rs.' + str(sold))
            
            sell_button.after(200, refresh_and_add)

        refresh_and_add()

