from tkinter import *
from tkinter import ttk
import sqlite3
import csv

def student_screen():

    # ---------------- WINDOW ----------------
    win = Tk()
    win.title("Student Records")
    win.geometry("900x520")

    # ---------------- THEME ----------------
    is_dark = False

    def toggle_theme():
        nonlocal is_dark
        bg = "#2b2b2b" if not is_dark else "white"
        fg = "white" if not is_dark else "black"

        win.config(bg=bg)
        for w in win.winfo_children():
            try:
                w.config(bg=bg, fg=fg)
            except:
                pass
        is_dark = not is_dark

    # ---------------- DATABASE ----------------
    def view_students(query="SELECT * FROM students", values=()):
        rows = table.get_children()
        for r in rows:
            table.delete(r)

        conn = sqlite3.connect("students.db")
        cur = conn.cursor()
        cur.execute(query, values)

        for row in cur.fetchall():
            table.insert("", END, values=row)

        conn.close()

    def get_performance(m):
        if m >= 75:
            return "Excellent"
        elif m >= 60:
            return "Good"
        elif m >= 40:
            return "Average"
        else:
            return "Needs Improvement"

    # ---------------- ADD ----------------
    def add_student():
        name = e_name.get()
        roll = e_roll.get()
        course = e_course.get()
        marks = e_marks.get()

        if name == "" or roll == "" or course == "" or marks == "":
            error_msg.config(text="All fields required")
            return

        try:
            marks = int(marks)
        except:
            error_msg.config(text="Marks must be number")
            return

        perf = get_performance(marks)

        conn = sqlite3.connect("students.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students(name, roll, course, marks, performance) VALUES(?,?,?,?,?)",
            (name, roll, course, marks, perf)
        )
        conn.commit()
        conn.close()

        clear_fields()
        error_msg.config(text="")
        view_students()

    # ---------------- DELETE ----------------
    def delete_student():
        selected = table.focus()
        if selected == "":
            error_msg.config(text="Select record to delete")
            return

        sid = table.item(selected)["values"][0]

        conn = sqlite3.connect("students.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id=?", (sid,))
        conn.commit()
        conn.close()

        clear_fields()
        view_students()

    # ---------------- UPDATE ----------------
    def update_student():
        if e_id.get() == "":
            error_msg.config(text="Select record to update")
            return

        try:
            marks = int(e_marks.get())
        except:
            error_msg.config(text="Marks must be number")
            return

        perf = get_performance(marks)

        conn = sqlite3.connect("students.db")
        cur = conn.cursor()
        cur.execute(
            "UPDATE students SET name=?, roll=?, course=?, marks=?, performance=? WHERE id=?",
            (e_name.get(), e_roll.get(), e_course.get(), marks, perf, e_id.get())
        )
        conn.commit()
        conn.close()

        view_students()

    # ---------------- SEARCH ----------------
    def search_student():
        key = search_entry.get()
        if key == "":
            view_students()
        else:
            view_students(
                "SELECT * FROM students WHERE name LIKE ?",
                ('%' + key + '%',)
            )

    # ---------------- FILTER ----------------
    def filter_performance():
        val = perf_filter.get()
        if val == "All":
            view_students()
        else:
            view_students(
                "SELECT * FROM students WHERE performance=?",
                (val,)
            )

    # ---------------- EXPORT CSV ----------------
    def export_csv():
        conn = sqlite3.connect("students.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        data = cur.fetchall()
        conn.close()

        with open("students.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Roll", "Course", "Marks", "Performance"])
            writer.writerows(data)

        error_msg.config(text="Exported to students.csv")

    # ---------------- FILL FORM ----------------
    def fill_form(event):
        selected = table.focus()
        if selected == "":
            return

        row = table.item(selected)["values"]
        clear_fields()

        e_id.insert(0, row[0])
        e_name.insert(0, row[1])
        e_roll.insert(0, row[2])
        e_course.insert(0, row[3])
        e_marks.insert(0, row[4])

    def clear_fields():
        e_id.delete(0, END)
        e_name.delete(0, END)
        e_roll.delete(0, END)
        e_course.delete(0, END)
        e_marks.delete(0, END)

    # ---------------- UI ----------------
    Label(win, text="ID").grid(row=0, column=0)
    Label(win, text="Name").grid(row=1, column=0)
    Label(win, text="Roll").grid(row=2, column=0)
    Label(win, text="Course").grid(row=3, column=0)
    Label(win, text="Marks").grid(row=4, column=0)

    e_id = Entry(win)
    e_name = Entry(win)
    e_roll = Entry(win)
    e_course = Entry(win)
    e_marks = Entry(win)

    e_id.grid(row=0, column=1)
    e_name.grid(row=1, column=1)
    e_roll.grid(row=2, column=1)
    e_course.grid(row=3, column=1)
    e_marks.grid(row=4, column=1)

    Button(win, text="Add", command=add_student).grid(row=5, column=0)
    Button(win, text="Update", command=update_student).grid(row=5, column=1)
    Button(win, text="Delete", command=delete_student).grid(row=5, column=2)
    Button(win, text="Export CSV", command=export_csv).grid(row=5, column=3)
    Button(win, text="Theme", command=toggle_theme).grid(row=0, column=6)

    error_msg = Label(win, text="", fg="red")
    error_msg.grid(row=6, column=0, columnspan=4)

    Label(win, text="Search Name").grid(row=0, column=3)
    search_entry = Entry(win)
    search_entry.grid(row=0, column=4)
    Button(win, text="Search", command=search_student).grid(row=0, column=5)

    Label(win, text="Filter").grid(row=1, column=3)
    perf_filter = StringVar()
    perf_filter.set("All")
    OptionMenu(win, perf_filter, "All", "Excellent", "Good", "Average", "Needs Improvement",
               command=lambda x: filter_performance()).grid(row=1, column=4)

    table = ttk.Treeview(win,
        columns=("ID","Name","Roll","Course","Marks","Performance"),
        show="headings", height=12)

    for col in ("ID","Name","Roll","Course","Marks","Performance"):
        table.heading(col, text=col)
        table.column(col, width=120)

    table.grid(row=7, column=0, columnspan=7, pady=10)
    table.bind("<<TreeviewSelect>>", fill_form)

    view_students()
    win.mainloop()
