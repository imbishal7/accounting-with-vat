from tkinter import *
from tkinter import messagebox
import datetime as addate
import nepali_datetime as datetime
import calendar
from time import strftime
from credentials import username
from credentials import password

# --------------Fonts--------------- #

huge_font = ('Comic Sans MS', 60, 'bold')
medium_font = ('Comic Sans MS', 49)
small_font = ('Comic Sans MS', 30)
tiny_font = ('Comic Sans MS', 20)
medium_lined = ('Imprint MT Shadow', 55, 'underline')
very_small = ('Comic Sans MS', 15)


# ---------------VARIABLES----------#
fcompany_name = 'My Company name in Lockscreen.py'
background = '#94ffd6'
date_bg = '#fff78a'
login_bg= '#70d7ff'

# ------------Formatting Company Name-----------#

partion_names = fcompany_name.split(' ')
if (len(partion_names)>3) and (len(partion_names)<=5):
    fcompany_name = ' '.join(partion_names[:2]) + "\n"+' '.join(partion_names[2:])
elif len(partion_names)>5:
    fcompany_name = ' '.join(partion_names[:3])+ '\n'+ ' '.join(partion_names[3:])


# ----------Lock Screen---------------#

class LockScreen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=background)
        self.controller = controller
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(5, weight=2)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(3, weight=1)

        head = Label(self, text=fcompany_name, font=huge_font, fg='#ffb536', bg=background)
        head.grid(row=2, column=2, sticky=NSEW,columnspan=3)

        date_frame = Frame(self, height=350, width=350, bg=date_bg, padx=40, pady=40, relief=GROOVE, bd=5)
        date_frame.grid(row=4, column=2, sticky=E)

        login_frame = Frame(self, height=250, width=500, bg=login_bg, padx=35, pady=35, relief=GROOVE, bd=5)
        login_frame.grid(row=4, column=4, sticky = W)

        clock = Label(date_frame, font=medium_font, fg='#3508ff', bg=date_bg)
        clock.pack()

        weekday = Label(date_frame, font=medium_font, fg='#711994', bg=date_bg)
        weekday.pack()

        dates = Label(date_frame, font=medium_font, fg='#711994', bg=date_bg)
        dates.pack()

# --------------Updating time and date ------------------#

        def update_label():
            current_time = strftime('%H: %M: %S')
            clock.configure(text=current_time)
            d = datetime.date.today()
            adate = addate.datetime.today()
            day = calendar.day_name[adate.weekday()]

            dates.configure(text=d)
            weekday.configure(text=day)

            weekday.after(80, update_label)
        update_label()

        unm = Label(login_frame, text='Username:', font=small_font, bg=login_bg, fg='grey')
        unm.place(x=5,y=5)
        pwd = Label(login_frame, text='Password:', font=small_font, bg=login_bg, fg='grey')
        pwd.place(x=5, y =60)

        un = Entry(login_frame, font=tiny_font, width=12)
        un.place(x=220, y=10)
        pw = Entry(login_frame, font=tiny_font, width=12, show='*')
        pw.place(x=220, y=70)

# --------------Login function------------#
        def login_f():
            u = un.get()
            p = pw.get()
            if u == username and p == password:
                controller.show_frame('StatementsPage')
            elif (u=='' or p==''):
                messagebox.showerror(title='Error', message='Please fill the username and password to login.')
            else:
                messagebox.showerror(title='Error', message='Wrong Credentials Provided')
            pw.delete(0, 'end')
            un.delete(0, 'end')
            
# ----------------Forget function(functionless)--------------#
        def popup():
            messagebox.showinfo(title='Help', message="The default username and password are 'root' and 'root'."
                                                      "You are requested to change them in credentials.py file."
                                                      "Also disable this warning from lockscreen.py > popup function"
                                                      " for security.")

        forgot = Button(login_frame, bg='red',fg='white', text='Forgot ?', font=tiny_font, height=1, width=8, command=popup)
        login = Button(login_frame, bg='green',fg='white', text='Login !', font=tiny_font, height=1, width=8, command=login_f)

        forgot.place(x=50, y=125)
        login.place(x=250, y=125)
