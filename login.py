from tkinter import *
import sqlite3

def login_screen():
    win = Tk()
    win.title("Login")
    win.geometry("300x200")

    Label(win, text="Student Performance System",
          font=("Arial", 12)).pack(pady=10)

    Label(win, text="Username").pack()
    username = Entry(win)
    username.pack()

    Label(win, text="Password").pack()
    password = Entry(win, show="*")
    password.pack()

    def check_login():
        conn = sqlite3.connect("students.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username.get(), password.get())
        )

        if cur.fetchone():
            win.destroy()
            import dashboard
            dashboard.dashboard_screen()

        else:
            Label(win, text="Invalid Login",
                  fg="red").pack()

        conn.close()

    Button(win, text="Login",
           command=check_login).pack(pady=10)

    win.mainloop()
