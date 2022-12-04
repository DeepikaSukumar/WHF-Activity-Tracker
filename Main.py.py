from tkinter import *
import sqlite3
from datetime import datetime
import timer

global count
count = 0

root = Tk()
root.title("Work From Home Activity Tracker")
width = 400
height = 280
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(None, None)
counter = 66600
running = False


# ==============================METHODS========================================
def database():
    global conn, cursor
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, "
        "password TEXT)")
    cursor.execute("SELECT * FROM `member` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `member` (username, password) VALUES('admin', 'admin')")
        conn.commit()


def login(event=None):
    database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? AND `password` = ?",
                       (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            homewindow()
            USERNAME.set("")
            PASSWORD.set("")
            lbl_text.config(text="")
        else:
            lbl_text.config(text="Invalid username or password. Try again!", fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close()


def time_in(event=None):
    def reset():
        global count
        count = 1
        t.set('00:00:00')

    def start():
        global count
        count = 0
        timer()

    def stop():
        global count
        count = 1

    def close():
        root.destroy()

    def timer():
        global count
        if count == 0:
            d = str(t.get())
            h, m, s = map(int, d.split(":"))
            h = int(h)
            m = int(m)
            s = int(s)
            if s < 59:
                s += 1
            elif s == 59:
                s = 0
                if m < 59:
                    m += 1
                elif m == 59:
                    m = 0
                    h += 1
            if h < 10:
                h = str(0) + str(h)
            else:
                h = str(h)
            if m < 10:
                m = str(0) + str(m)
            else:
                m = str(m)
            if s < 10:
                s = str(0) + str(s)
            else:
                s = str(s)
            d = h + ":" + m + ":" + s
            t.set(d)
            if count == 0:
                root.after(1000, timer)
    t = StringVar()
    t.set("00:00:00")
    lb = Label(root, textvariable=t, font="Times 40 bold", bg="white")
    bt1 = Button(root, text="Start", command=start, font="Times 12 bold", bg="#F88379")
    bt2 = Button(root, text="Break in", command=stop, font="Times 12 bold", bg="#F88379")
    bt3 = Button(root, text="Reset", command=reset, font="Times 12 bold", bg="#DE1738")
    bt4 = Button(root, text="Exit", command=close, font="Times 12 bold", bg="#DE1738")
    lb.place(x=160, y=10)
    bt1.place(x=120, y=100)
    bt2.place(x=220, y=100)
    bt3.place(x=320, y=100)
    bt4.place(x=420, y=100)
    label = Label(root, text="", font="Times 40 bold")
    root.configure(bg='white')


def homewindow():
    global Home
    root.withdraw()
    Home = Toplevel()
    Home.title("Work From Home Activity Tracker")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.resizable(None, None)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    Label(Home, text="Welcome Admin!", font=('times new roman', 20)).pack()
    Button(Home, text='Time In', command=time_in).pack(pady=19.5, fill=X)
    Button(Home, text='Log Out', command=back).pack(pady=20, fill=X)


def back():
    Home.destroy()
    root.deiconify()


# ==============================VARIABLES======================================
USERNAME = StringVar()
PASSWORD = StringVar()

# ==============================FRAMES=========================================
Top = Frame(root, bd=2, relief=RIDGE)
Top.pack(side=TOP, fill=X)
Form = Frame(root, height=200)
Form.pack(side=TOP, pady=20)

# ==============================LABELS=========================================
lbl_title = Label(Top, text="Work From Home Activity Tracker", font=('arial', 15))
lbl_title.pack(fill=X)
lbl_username = Label(Form, text="Username:", font=('arial', 14), bd=15)
lbl_username.grid(row=0, sticky="e")
lbl_password = Label(Form, text="Password:", font=('arial', 14), bd=15)
lbl_password.grid(row=1, sticky="e")
lbl_text = Label(Form)
lbl_text.grid(row=2, columnspan=2)

# ==============================ENTRY WIDGETS==================================
username = Entry(Form, textvariable=USERNAME, font=14)
username.grid(row=0, column=1)
password = Entry(Form, textvariable=PASSWORD, show="*", font=14)
password.grid(row=1, column=1)

# ==============================BUTTON WIDGETS=================================
btn_login = Button(Form, text="Login", width=45, command=login)
btn_login.grid(pady=25, row=3, columnspan=2)
btn_login.bind('<Return>', login)

# ==============================INITIALIZATION==================================
if __name__ == '__main__':
    root.mainloop()
