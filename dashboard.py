from tkinter import *

def dashboard_screen():
    win = Tk()
    win.title("Dashboard")
    win.geometry("400x300")

    Label(
        win,
        text="Student Performance System",
        font=("Arial", 16)
    ).pack(pady=30)

    def open_student():
        import student
        student.student_screen()

    Button(
        win,
        text="Manage Students",
        width=25,
        command=open_student
    ).pack(pady=10)

    Button(
        win,
        text="Exit",
        width=25,
        command=win.destroy
    ).pack(pady=10)

    win.mainloop()
