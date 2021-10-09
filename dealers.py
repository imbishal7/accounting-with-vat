from tkinter import *
from functions import *
from tkinter import ttk
from tkinter import messagebox

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

back = '#ffe0bf'


class Dealers(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        func_frame = Frame(self, height=200,padx=10, pady=10, bg=back)
        func_frame.pack(side=TOP, fill=X)
        func_frame.grid_columnconfigure(3, weight=2)

        head = Label(func_frame, text='Dealers', font=medium_lined, bg=back, fg='dark blue')
        head.grid(row=1, column=1, columnspan=2)

        statementsb = Button(func_frame, relief=GROOVE, bd=4, text='Statements', bg='yellow', fg='brown', font=tiny_font,
                       height=1, width=10, command=lambda: controller.show_frame('StatementsPage'))
        statementsb.grid(row=2, column=1, padx=5)

        custb = Button(func_frame, relief=GROOVE, bd=4, text='Customers', bg='green', fg='white', font=tiny_font, height=1,
                       width=10, command=lambda: controller.show_frame('Customers'))
        custb.grid(row=2, column=2)

        payables = Label(func_frame, font=medium_font, bg='#ff8d36', fg='white', padx=25, pady=10,
                            relief=RIDGE, bd=5, width=12)
        payables.grid(row=1, column=5, sticky=NE, padx=5)

        r_text = Label(func_frame, text='Payables:', font=head_text,fg='purple', bg=back)
        r_text.grid(row=1, column=4, sticky=NE, padx=5)

        add_button = Button(func_frame, text='+Add', font=tiny_font, bg='#2930ff', fg='white', bd=4, relief=GROOVE,
                            width=6, command=lambda :get_details_add())
        add_button.grid(row=2, column=5, padx=2, pady=5)
        delete_button = Button(func_frame, text='Delete', font=tiny_font, bg='#2930ff', fg='white', bd=4, relief=GROOVE,
                             width=6, command=lambda:get_details_delete())
        delete_button.grid(row=2, column=5,padx=2, sticky=E, pady=5)

        lock_button = Button(func_frame, text='Lock', font=tiny_font, bg='light green', fg='black', bd=4, relief=GROOVE,
                             width=4, command=lambda: controller.show_frame('LockScreen'))
        lock_button.grid(row=2, column=5, pady=10, sticky=W)

        def get_details_delete():
            bg='silver'
            delete_window = Toplevel(self, bg=bg, padx=10, pady=10)
            delete_window.title('Delete Dealer')
            delete_window.geometry('600x300')

            Label(delete_window, text='Enter Dealer Details:', font=small_font, bg=bg).grid(row=1, column=1,columnspan=2,sticky='nsew')
            Label(delete_window, text='Name:', font=tiny_font, bg=bg).grid(row=2, column=1, sticky=NSEW)
            Label(delete_window, text='Address:', font=tiny_font, bg=bg).grid(row=3, column=1, sticky='nsew')

            name = Entry(delete_window, font=tiny_font)
            address = Entry(delete_window, font=tiny_font)
            name.grid(row=2, column=2, sticky='nsew')
            address.grid(row=3, column=2, sticky='nsew')

            delete_b = Button(delete_window, font=small_font, text='Delete', bg='orange',
                              command=lambda: delete_dealer(), width=2, height=1)
            delete_b.grid(row=4, column=2, sticky='nsew', padx=10, pady=10)

            def delete_dealer():
                n = name.get().upper()
                ad = address.get().upper()
                delete_someone(n,ad,'Dealer')
                delete_window.destroy()

        def get_details_add():
            bg='#aebefc'
            add_window = Toplevel(self, bg=bg)
            add_window.title('Add Dealer')
            add_window.geometry('600x350')

            Label(add_window, text='Enter Dealer Details:', font=small_font, bg=bg).grid(row=1, column=1,
                                                                                           columnspan=2, sticky=NSEW)
            Label(add_window, text='Name:', font=tiny_font, bg=bg).grid(row=2, column=1, sticky='nsew')
            Label(add_window, text='Address:', font=tiny_font, bg=bg).grid(row=3, column=1, sticky='nsew')
            Label(add_window, text='Contacts:', font=tiny_font, bg=bg).grid(row=4, column=1, sticky='nsew')

            name = Entry(add_window, font=tiny_font)
            address = Entry(add_window, font=tiny_font)
            contacts = Entry(add_window, font=tiny_font)
            name.grid(row=2, column=2, sticky='nsew')
            address.grid(row=3, column=2, sticky='nsew')
            contacts.grid(row=4, column=2, sticky='nsew')

            add_b = Button(add_window, text='Add', font=small_font, bg='#aeff2b', command=lambda: add_dealer())
            add_b.grid(row=5, column=2, sticky='nsew', padx=10, pady=10)

            def add_dealer():
                n = name.get().upper()
                ad = address.get().upper()
                con = contacts.get()
                if "" not in [n,ad,con]:
                    Dealer(n,ad,con).add()
                else:
                    messagebox.showerror(title='Error', message='Please fill all fields')
                add_window.destroy()
                refresh_and_add_all()

# ---------------------------------------Table -----------------------------------------#
# --------------------show info function-----------------#

        def show_info(event):
            for selected_item in custs.selection():
                item = custs.item(selected_item)
                someone=item['values']
                name = someone[0]
                address = someone[1]

                info =evaluate(name,address,'Dealer')
                try:
                    balance = info[2]-info[1]
                except:
                    balance='NA'
                try:
                    contact = details(name,address,'Dealer')
                except:
                    contact = 'Not available'

                info_window = Toplevel(self)
                info_window.title('About '+name)
                info_window.geometry('1150x700')


                bg = '#fdffc7'

                head_frame = Frame(info_window, bg=bg)
                head_frame.pack(fill=X, expand=True)

                Label(head_frame, text='All Transactions of '+name, font=medium_lined,bg=bg, fg='magenta', bd=4,).grid(row=1, column=1, columnspan=10,sticky='nsew', padx=10, pady=10)
                Label(head_frame, text='Phone:' + str(contact), font=small_font, bg=bg,fg='brown').grid(row=2, column=1,sticky='nw', padx=10, pady=10)
                Label(head_frame, text='Address:' + str(address), font=small_font, bg=bg,fg='brown').grid(row=3, sticky='nw',column=1, padx=10, pady=10)
                Label(head_frame, text='Balance:', font=small_font, bg=bg,fg='brown').grid(row=4, column=1, sticky='nw', padx=10, pady=10)
                Label(head_frame, text='Rs.' + str(balance), font=medium_font, bd=5, bg='#fa582f', fg='white',relief=GROOVE, width=10).grid(row=4, column=2, sticky='nw', padx=10, pady=10)

                info_frame = Frame(info_window, bg='yellow', relief=GROOVE, bd=5)
                info_frame.pack(padx=10, pady=10, fill=BOTH, expand=True, side=BOTTOM)

                stats = ttk.Treeview(info_frame, columns=(1, 2, 3, 4, 5, 6, 7), show='headings', style='Treeview')
                stats.pack(side=LEFT, fill=BOTH, expand=True)

                scrollbar = ttk.Scrollbar(info_frame, orient=VERTICAL, command=stats.yview)
                stats.configure(yscroll=scrollbar.set)
                scrollbar.pack(side=RIGHT, fill=Y)

                headings = ['Date', 'Time', 'Ref. No.', 'Name', 'Remarks', 'Debit', 'Credit']
                for h in headings:
                    stats.heading(headings.index(h) + 1, text=h)
                    if h in ['Remarks', 'Debit', 'Credit', 'Date']:
                        stats.column(headings.index(h) + 1, minwidth=50, width=180)
                    elif h == 'Name':
                        stats.column(headings.index(h) + 1, minwidth=50, width=200)
                    else:
                        stats.column(headings.index(h) + 1, minwidth=50, width=120)

                style = ttk.Style()
                style.theme_use('default')
                style.map('Treeview')
                style.configure('Treeview', font=tiny_font, rowheight=40)
                style.configure('Treeview.Heading', font=(tree_font))

                def refresh_info():
                    stats.delete(*stats.get_children())
                    transactions = get_all_for(name,address, 'Dealer')
                    for i in range(len(transactions)):
                        statements = transactions[i]
                        stats.insert('', index=i, values=statements)
                refresh_info()


# ------------------------------------show table function ------------#

        table_frame = Frame(self, bg='yellow', relief=GROOVE, bd=5)
        table_frame.pack(side=TOP, padx=10, pady=10, fill=BOTH, expand=True)

        headings=['Name','Address','Debit','Credit','Balance']

        custs = ttk.Treeview(table_frame, columns=(1,2,3,4,5), show='headings', style='Treeview')
        custs.pack(side=LEFT, fill=BOTH, expand=True)
        custs.bind('<<TreeviewSelect>>', show_info)

        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=custs.yview())
        custs.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        for h in headings:
            custs.heading(headings.index(h)+1, text=h)
            if h =='Name' or h=='Address':
                custs.column(headings.index(h)+1, minwidth=200, width=300)
            else:
                custs.column(headings.index(h)+1, minwidth=50, width=150)

        def fixed_map(option):
            return [elm for elm in style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]

        style = ttk.Style()
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
        style.theme_use('default')
        style.map('Treeview')
        style.configure('Treeview', font=tiny_font)
        custs.tag_configure('cleared', background='#73ffa6')
        custs.tag_configure('due', background='#ff4766')
        custs.tag_configure('unknown', background='#d5ccff')


        def refresh_and_add_all():
            custs.delete(*custs.get_children())
            dealers = all_customers_dealers_with_address('Dealer')
            for i in range(len(dealers)):
                info = evaluate(dealers[i][0], dealers[i][1], 'Dealer')
                name=dealers[i][0]
                address=info[0]
                debit=info[1]
                credit=info[2]
                if debit !='NA':
                    balance = credit-debit
                else:
                    balance = 'NA'
                values =[name,address, debit, credit, balance]
                if balance == 0:
                    custs.insert('', index=i, values=values, tags=('cleared',))
                elif balance == 'NA':
                    custs.insert('', index=i, values=values, tags=('unknown',))
                else:
                    custs.insert('', index=i, values=values, tags=('due',))

            to_pay = receivables_payables('Dealer')
            payables.config(text='Rs.' + str(to_pay))
            add_button.after(200, refresh_and_add_all)

        refresh_and_add_all()
