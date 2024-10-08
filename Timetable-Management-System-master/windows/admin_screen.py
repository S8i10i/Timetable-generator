import tkinter as tk
from tkinter import messagebox
import sys
import os
import threading
import sqlite3
from tkinter import ttk

def run_sub():
    os.system('pythonw windows\\subjects.py')

def run_fac():
    os.system('pythonw windows\\faculty.py')

def run_stud():
    os.system('pythonw windows\\student.py')

def run_sch():
    os.system('pythonw windows\\scheduler.py')

def run_tt_s():
    os.system('pythonw windows\\timetable_stud.py')

def run_tt_f():
    os.system('pythonw windows\\timetable_fac.py')

def run_request():
    messagebox.showinfo("Message", "Leave Details")

    def connect():
        con1 = sqlite3.connect(r'files/timetable.db')

    def View():
        os.system('pythonw windows\\scheduler.py')

    root = tk.Tk()
    root.configure(bg="black")  # Set the background color to black

    tree = ttk.Treeview(root, column=("fid", "fromdate", "todate", "reason"), show='headings')
    tree.column("#1", anchor=tk.CENTER)
    tree.heading("#1", text="ID")
    tree.column("#2", anchor=tk.CENTER)
    tree.heading("#2", text="FROMDATE")
    tree.column("#3", anchor=tk.CENTER)
    tree.heading("#3", text="TODATE")
    tree.column("#4", anchor=tk.CENTER)
    tree.heading("#4", text="REASON")
    tree.pack()

    con1 = sqlite3.connect(r'files/timetable.db')
    cur1 = con1.cursor()
    cur1.execute("SELECT FID,FROMDATE,TODATE,REASON FROM LEAVE")
    rows = cur1.fetchall()
    for row in rows:
        print(row)
        tree.insert("", tk.END, values=row)
    con1.close()

    button1 = tk.Button(root, text="RESCHEDULE CLASSES", command=View)
    button1.pack(pady=10)
    root.mainloop()

ad = tk.Tk()
ad.geometry('1920x1080')
ad.configure(bg="black")  # Set the background color to black

ad.title('Administrator')

admin_label = tk.Label(
    ad,
    text='A D M I N I S T R A T O R',
    font=('areal', 30, 'bold'),
    pady=10,
    bg="black",
    fg="white"
)
admin_label.place(x=560,y=100) 



leave_button = tk.Button(
    ad,
    text='LEAVE REQUESTS',
    font=('Calibri'),
    command=run_request,
    bg="red",
    fg="white"
)
leave_button.place(x=700,y=180) 

modify_frame = tk.LabelFrame(text='MODIFY', font=('Calibri'), padx=30, bg="black", fg="white")
modify_frame.place(x=580, y=250)

tk.Button(
    modify_frame,
    text='SUBJECTS',
    font=('Calibri'),
    command=run_sub,
    bg="green",
    fg="white"
).pack(pady=20)

tk.Button(
    modify_frame,
    text='FACULTIES',
    font=('Calibri'),
    command=run_fac,
    bg="green",
    fg="white"
).pack(pady=20)

tk.Button(
    modify_frame,
    text='STUDENTS',
    font=('Calibri'),
    command=run_stud,
    bg="green",
    fg="white"
).pack(pady=20)

tt_frame = tk.LabelFrame(text='TIME TABLE', font=('Consolas'), padx=20, bg="black", fg="white")
tt_frame.place(x=780, y=250)

tk.Button(
    tt_frame,
    text='SCHEDULE PERIODS',
    font=('Calibri'),
    command=run_sch,
    bg="green",
    fg="white"
).pack(pady=20)

tk.Button(
    tt_frame,
    text='VIEW SECTION-WISE',
    font=('Calibri'),
    command=run_tt_s,
    bg="green",
    fg="white"
).pack(pady=20)

tk.Button(
    tt_frame,
    text='VIEW FACULTY-WISE',
    font=('Calibri'),
    command=run_tt_f,
    bg="green",
    fg="white"
).pack(pady=20)

tk.Button(
    ad,
    text='QUIT',
    font=('Calibri'),
    bg='yellow',
    fg='black',
    command=ad.destroy
).place(x=750, y=580)

ad.mainloop()