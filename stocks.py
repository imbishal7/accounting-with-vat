from tkinter import *
from tkinter import messagebox
from datetime import date
from time import strftime
from functions import *
from tkinter import ttk
from functions_vat import *


# --------------Fonts--------------- #
medium_font = ('Footlight MT Light', 55)
medium_lined = ('Imprint MT Shadow', 55, 'underline')
small_font = ('Berlin Sans FB', 30)
tiny_font = ('Times New Roman', 20)
very_small = ('Comic Sans MS', 17)
tree_font = ('Georgia', 20)
dialog_font = ("Agency FB", 20)

# ---------------Background for statements page------------#
bg = '#fdffc7'


# -------------Statements Page----------#

class StocksPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller
# -----------------Funtions frame ---------------#
        func_frame = Frame(self, height=200, padx=10, pady=10, bg=bg)
        func_frame.pack(side=TOP, fill=X)

        func_frame.grid_columnconfigure(3, weight=1)
        head = Label(func_frame, text='Stocks', fg='dark blue', font=medium_lined, bg=bg)
        head.grid(row=1, column=1, columnspan=2)

        salesb = Button(func_frame, relief=GROOVE, bd=4, text='Sales', bg='green', fg='white', font=tiny_font,height=1, width=10, command=lambda: controller.show_frame('Sales'))
        salesb.grid(row=2, column=1, padx=5)

        purchasesb = Button(func_frame, relief=GROOVE, bd=4, text='Purchases', bg='red',fg='white', font=tiny_font,height=1, width=10, command=lambda: controller.show_frame('Purchases'))
        purchasesb.grid(row=2, column=2, padx=5)
        
        sta = Button(func_frame, relief=GROOVE, bd=4, text='Statements', bg='silver',fg='black', font=tiny_font,height=1, width=10, command=lambda: controller.show_frame('StatementsPage'))
        sta.grid(row=2, column=3, sticky='W', padx=5)


        add_button = Button(func_frame, text='± Change Stocks', font=tiny_font, bg='#2930ff', fg='white', bd=4, relief=GROOVE, width=14, command=lambda: get_entry())
        add_button.grid(row=2,column=6, pady=10, padx=10)

        lock_button = Button(func_frame, text='Lock', font=tiny_font, bg='light green', fg='black', bd=4, relief=GROOVE, width=4, command=lambda :controller.show_frame('LockScreen'))
        lock_button.grid(row=2, column=5, pady=10, sticky=W, padx=10)

        refresh_button = Button(func_frame, text='Refresh', font=tiny_font, bg='sky blue', bd=4, relief=GROOVE, command=lambda:refresh_and_add())
        refresh_button.grid(row=2,column=4, pady=10, sticky=E, padx=10)

        def get_delete_stocks():
            bg='silver'
            delete_window = Toplevel(self, bg=bg, padx=10,pady=10)
            delete_window.title('Delete Stock')
            delete_window.geometry('600x300')

            Label(delete_window, text='Enter following Details:', font=small_font,bg=bg).grid(row=1, column=1,columnspan=2, sticky='nsew')
            Label(delete_window, text='Product:', font=tiny_font,bg=bg).grid(row=2,column=1,sticky=NSEW)
            

            product = Entry(delete_window, font=tiny_font)
            product.grid(row=2, column=2, sticky='nsew')

            delete_b = Button(delete_window,font=small_font, text='Delete',bg='orange',command=lambda:delete_stock(), width=2, height=1)
            delete_b.grid(row=4, column=2,sticky='nsew',padx=10, pady=10)

            def delete_stock():
                n = product.get().upper()
                delete_from_stocks(n)
                delete_window.destroy()
                refresh_and_add()
            
        delete_stock_button =  Button(func_frame, text='Delete', font=tiny_font, bg='orange', bd=4, relief=GROOVE, command=lambda:get_delete_stocks())
        delete_stock_button.grid(row=2, column=3, sticky=E)

# ------------Add Button-----------#
        def get_entry():
            global entry_window
            bg = "#e1ffbd"
            entry_window = Toplevel(self, bg=bg, padx=20, pady=20)
            entry_window.title('Add Stocks Unverified')

            lan = Label(entry_window, text='Enter following details:', font=small_font, bg = bg)
            lan.grid(row=1, column=1, columnspan=4)

            Label(entry_window, text='Product Name:', font=tree_font, bg = bg).grid(row=3, column=1)
            Label(entry_window, text='Quantity:', font=tree_font, bg = bg).grid(row=5, column=1)
            Label(entry_window, text='Rate:', font=tree_font, bg = bg).grid(row=6, column=1)
            Label(entry_window, text='Actual Rate:', font=tree_font, bg = bg).grid(row=7, column=1)
            

            n = StringVar()
            name = ttk.Combobox(entry_window, width=19, textvariable=n, font=tree_font)
            name['values'] = all_stocks()
            
            quantity = Entry(entry_window, font=tree_font)
            rate = Entry(entry_window, font=tree_font)
            actual_rate = Entry(entry_window, font=tree_font)

            quantity.grid(row=5, column=2)
            name.grid(row=3, column=2)
            rate.grid(row=6, column=2)
            actual_rate.grid(row=7, column=2)

            add_buttn = Button(entry_window, text='CONFIRM', font=small_font, bd=5, bg='#b494ff', relief=GROOVE,
                               command=lambda: add_to_stock())
            add_buttn.grid(row=8, column=1, columnspan=4)
            global values

            values = [name, quantity, rate, actual_rate]

        def add_to_stock():
            
            entered_values = []
            for i in values:
                value = i.get().upper()
                entered_values.append(value)

            if "" not in entered_values:
                Stocks(entered_values[0], entered_values[1], entered_values[2], entered_values[3]).add_stock()
            else:
                messagebox.showerror(title='Error', message='Please fill all fields')
            entry_window.destroy()
            refresh_and_add()
            
# --------------Table Scroll-----------------#

        table_frame = Frame(self, bg='yellow', relief=GROOVE, bd=5)
        table_frame.pack(side=TOP, padx=10, pady=10, fill=BOTH, expand=True)

        stats =ttk.Treeview(table_frame, columns=(1,2,3,4), show='headings', style='Treeview')
        stats.pack(side=LEFT,fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=stats.yview)
        stats.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        headings = ['Product','Quantity', 'VAT Rate','Selling Rate']
        for h in headings:
            stats.heading(headings.index(h)+1, text=h)
            if h in ['VAT Rate','Selling Rate','Quantity']:
                stats.column(headings.index(h)+1, minwidth=50, width=150)
            else:
                stats.column(headings.index(h)+1, minwidth=50, width=300)


        style = ttk.Style()
        style.theme_use('default')
        style.map('Treeview')
        style.configure('Treeview', font=tiny_font, rowheight=40)
        style.configure('Treeview.Heading', font=(tree_font))

        def refresh_and_add():
            stats.delete(*stats.get_children())
            transactions = all_stocks_detail()
            for i in range(len(transactions)):
                statements = transactions[i]
                stats.insert('', index=i, values=statements)
        refresh_and_add()
