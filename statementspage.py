from tkinter import *
from tkinter import messagebox
from nepali_datetime import date
from time import strftime
from functions import *
from tkinter import ttk

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

class StatementsPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller
# -----------------Funtions frame ---------------#
        func_frame = Frame(self, height=200, padx=10, pady=10, bg=bg)
        func_frame.pack(side=TOP, fill=X)

        func_frame.grid_columnconfigure(3, weight=2)
        head = Label(func_frame, text='Statements', fg='dark blue', font=medium_lined, bg=bg)
        head.grid(row=1, column=1, columnspan=2)

        custb = Button(func_frame, relief=GROOVE, bd=4, text='Customers', bg='green', fg='white', font=tiny_font,height=1, width=10, command=lambda: controller.show_frame('Customers'))
        custb.grid(row=2, column=1)
        dealb = Button(func_frame, relief=GROOVE, bd=4, text='Dealers', bg='red',fg='white', font=tiny_font,height=1, width=10, command=lambda: controller.show_frame('Dealers'))
        dealb.grid(row=2, column=2)
        stocksb = Button(func_frame, relief=GROOVE, bd=4, text='Stocks', bg='silver',fg='black', font=tiny_font,height=1, width=10, command=lambda: controller.show_frame('StocksPage'))
        stocksb.grid(row=2, column=3)

        sold = Label(func_frame, font=medium_font, bg='#52c433', fg='white', padx=25,pady=10,relief=RIDGE, bd=5, width=10)
        sold.grid(row=1, column=4, rowspan=1, sticky=NE, padx=5)
        bought = Label(func_frame, font=medium_font, bg='#fa582f', fg='white', padx=25, pady=10, bd=5,relief=RIDGE, width=10)
        bought.grid(row=1, column=5, rowspan=1, sticky=NE, padx=5)

        add_button = Button(func_frame, text='+Add', font=tiny_font, bg='#2930ff', fg='white', bd=4, relief=GROOVE, width=6, command=lambda: get_entry())
        add_button.grid(row=2,column=5, pady=10)
        delete_button = Button(func_frame, text='Delete', font=tiny_font, bg='#2930ff', fg='white', bd=4, relief=GROOVE, width=6, command=lambda : delete_func())
        delete_button.grid(row=2, column=5, pady=10, sticky=E)

        lock_button = Button(func_frame, text='Lock', font=tiny_font, bg='light green', fg='black', bd=4, relief=GROOVE, width=4, command=lambda :controller.show_frame('LockScreen'))
        lock_button.grid(row=2, column=5, pady=10, sticky=W)

# ---------------Delete Button-------------#

        def delete_func():
            global pop
            global reff, namm
            bg='#ffeebd'
            pop = Toplevel(self, bg=bg, padx=20, pady=20)
            pop.title('Delete Statement')

            Label(pop, text='Enter reference no. and name of whose\n statement is to be deleted.', font = small_font, bg=bg).grid(row=0, column = 0, columnspan = 2, sticky = 'NSEW' )
            Label(pop, text='Reference NO.', font = tree_font,bg=bg).grid(row = 1, column =0, sticky = 'NSEW')
            Label(pop, text='Name', font = tree_font,bg=bg).grid(row = 2, column =0, sticky = 'NSEW')

            reff = Entry(pop, width=10, font=tree_font)
            reff.grid(row=1, column=1, sticky=NSEW)
            namm = Entry(pop, width=10, font=tree_font)
            namm.grid(row=2, column=1, sticky=NSEW)
            confirm_button = Button(pop, text='Delete!',padx=10,pady=10,bg='orange' ,font=small_font,bd=3, relief = GROOVE, command = lambda :get_to_delete())
            confirm_button.grid(row = 5,column = 1, columnspan =2, sticky=S)

            def get_to_delete():
                r = reff.get().upper()
                n = namm.get().upper()
                delete_transaction(r,n)
                pop.destroy()
                refresh_and_add()


# ------------Add Button-----------#
        def get_entry():
            global entry_window
            bg = "#e1ffbd"
            entry_window = Toplevel(self, bg=bg, padx=20, pady=20)
            entry_window.title('Add Transaction')

            lan = Label(entry_window, text='Enter transaction details:', font=small_font, bg = bg)
            lan.grid(row=1, column=1, columnspan=4)

            time_l = Label(entry_window, text='Time:', font=tree_font, bg = bg).grid(row=2, column=1)
            date_l = Label(entry_window, text='Date:', font=tree_font, bg = bg).grid(row=2, column=3)

            ref_l = Label(entry_window, text='Ref. No.', font=tree_font, bg = bg).grid(row=3, column=1)
            name_l = Label(entry_window, text='Name:', font=tree_font, bg = bg).grid(row=4, column=1)
            address_l = Label(entry_window, text='Address:', font=tree_font, bg = bg).grid(row=4, column=3)
            remarks_l = Label(entry_window, text='Remarks:', font=tree_font, bg = bg).grid(row=3, column=3)
            debit_l = Label(entry_window, text='Debit', font=tree_font, bg = bg).grid(row=6, column=1)
            credit_l = Label(entry_window, text='Credit', font=tree_font, bg = bg).grid(row=6, column=3)

            tdate = Entry(entry_window, font=tree_font)
            tdate.insert(0, date.today())
            ttime = Entry(entry_window, font=tree_font)
            ttime.insert(0, strftime('%H: %M'))
            n = StringVar()

            ref = Entry(entry_window, font=tree_font)
            name = ttk.Combobox(entry_window, width=19, textvariable=n, font=tree_font)
            name['values'] = get_all_names()

            address = Entry(entry_window, font=tree_font)
            remarks = Entry(entry_window, font=tree_font)
            debit = Entry(entry_window, font=tree_font)
            credit = Entry(entry_window, font=tree_font)

            var = IntVar()

            def selection():
                global ttype
                ttype='None'
                choice = var.get()
                if choice == 1:
                    ttype = 'Customer'
                elif choice ==2:
                    ttype = 'Dealer'
                return ttype
            def callback(eventObject):
                
                name = eventObject.widget.get()
                addr =gimme_address(name)
                address.insert(0, addr)                
            name.bind("<<ComboboxSelected>>", callback)

            cradio = Radiobutton(entry_window, text='Customer', variable = var, value = 1, command=selection, font=tree_font,bg=bg)
            dradio = Radiobutton(entry_window, text='Dealer', variable = var, value = 2, command = selection,font=tree_font,bg= bg)

            ttime.grid(row=2, column=2)
            tdate.grid(row=2, column=4)
            ref.grid(row=3, column=2)
            name.grid(row=4, column=2)
            address.grid(row=4, column=4)
            remarks.grid(row=3, column=4)
            debit.grid(row=6, column=2)
            credit.grid(row=6, column=4)
            cradio.grid(row=7, column=2)
            dradio.grid(row=7, column =4)

            add_buttn = Button(entry_window, text='CONFIRM', font=small_font, bd=5, bg='#b494ff', relief=GROOVE,
                               command=lambda: get_to_add())
            add_buttn.grid(row=8, column=1, columnspan=4)
            global values
            ttype=selection()
            values = [tdate, ttime, ref, name, address, 'ttype', remarks, debit, credit]

        def get_to_add():
            entered_values = []

            for i in values:
                if str(i) =='ttype':
                    value = ttype
                else:
                    value = i.get().upper()
                entered_values.append(value)
            if "" not in entered_values:
                Person(entered_values[0], entered_values[1], entered_values[2], entered_values[3], entered_values[4],
                       entered_values[5],
                       entered_values[6], entered_values[7], entered_values[8]).add()
            else:
                messagebox.showerror(title='Error', message='Please fill all fields')
            entry_window.destroy()
            refresh_and_add()

        def update_text():
            debit = debit_credit()[0]
            credit = debit_credit()[1]
            sold.config(text=debit)
            bought.config(text=credit)
            delete_button.after(1000, update_text)
        update_text()
# --------------Table Scroll-----------------#

        table_frame = Frame(self, bg='yellow', relief=GROOVE, bd=5)
        table_frame.pack(side=TOP, padx=10, pady=10, fill=BOTH, expand=True)

        stats =ttk.Treeview(table_frame, columns=(1,2,3,4,5,6,7,8), show='headings', style='Treeview')
        stats.pack(side=LEFT,fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=stats.yview)
        stats.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        headings = ['Date','Time','Ref. No.', 'Name','Type','Remarks','Debit','Credit']
        for h in headings:
            stats.heading(headings.index(h)+1, text=h)
            if h in ['Debit','Credit','Date']:
                stats.column(headings.index(h)+1, minwidth=50, width=120)
            elif h=='Name' or h =='Remarks':
                stats.column(headings.index(h)+1, minwidth=50, width=250)
            else:
                stats.column(headings.index(h)+1, minwidth=50, width=100)


        style = ttk.Style()
        style.theme_use('default')
        style.map('Treeview')
        style.configure('Treeview', font=tiny_font, rowheight=40)
        style.configure('Treeview.Heading', font=(tree_font))

        def refresh_and_add():
            stats.delete(*stats.get_children())
            transactions = get_all()
            for i in range(len(transactions)):
                statements = transactions[i]
                stats.insert('', index=i, values=statements)
        refresh_and_add()


