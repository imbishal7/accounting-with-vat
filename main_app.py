from financial_year import check_year
try:
    check_year()
except:
    print('No Database Found')
    
from lockscreen import LockScreen
from tkinter import *
from customers import Customers
from dealers import Dealers
from statementspage import StatementsPage
from stocks import StocksPage
from purchases import Purchases
from sales import Sales
from lockscreen import fcompany_name
from tkinter import ttk
# ------------- MAIN APP ----------#


class MainApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Dealers, StatementsPage, Customers, LockScreen, StocksPage, Purchases, Sales):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame('LockScreen')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == '__main__':
    app = MainApp()
    app.option_add("*TCombobox*Listbox*Font", ('Times New Roman', 18))

    app.title(fcompany_name)
    try:
        app.state('zoomed')
    except:
        pass
    try:
        app.iconbitmap('logo.ico')
    except:
        print('No icon file found')
    app.mainloop()
