import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os, sys
sys.path.insert(0, 'windows/')
import timetable_stud
import timetable_fac
import sqlite3




def challenge():
    conn = sqlite3.connect(r'files/timetable.db')
    user = str(combo1.get())

    if user == "Student":
        cursor = conn.execute(f"SELECT PASSW, SECTION, NAME, ROLL FROM STUDENT WHERE SID='{id_entry.get()}'")
        cursor = list(cursor)

        if len(cursor) == 0:
            messagebox.showwarning('Bad id', 'No such user found!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Bad pass', 'Incorrect Password!')
        else:
            nw = tk.Tk()
            nw.configure(bg='#2c3e50')
            tk.Label(
                nw,
                text=f'{cursor[0][2]}\tSection: {cursor[0][1]}\tRoll No.: {cursor[0][3]}',
                font=('Arial', 14, 'bold'),
                fg='white',
                bg='#2c3e50'
            ).pack(pady=20)
            m.destroy()
            timetable_stud.student_tt_frame(nw, cursor[0][1])
            nw.mainloop()

    elif user == "Faculty":
        cursor = conn.execute(f"SELECT PASSW, INI, NAME, EMAIL FROM FACULTY WHERE FID='{id_entry.get()}'")
        cursor = list(cursor)

        if len(cursor) == 0:
            messagebox.showwarning('Bad id', 'No such user found!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Bad pass', 'Incorrect Password!')
        else:
            nw = tk.Tk()
            nw.configure(bg='#2c3e50')
            tk.Label(
                nw,
                text=f'{cursor[0][2]} ({cursor[0][1]})\tEmail: {cursor[0][3]}',
                font=('Arial', 14, 'bold'),
                fg='white',
                bg='black'
            ).pack(pady=20)
            m.destroy()
            timetable_fac.fac_tt_frame(nw, cursor[0][1])
            nw.mainloop()

    elif user == "Admin":
        if id_entry.get() == 'admin' and passw_entry.get() == 'admin':
            m.destroy()
            os.system('python windows\\admin_screen.py')
        else:
            messagebox.showerror('Bad Input', 'Incorrect Username/Password!')

def show_passw():
    if passw_entry['show'] == "●":
        passw_entry['show'] = ""
        B1_show['text'] = '●'
        B1_show.update()
    elif passw_entry['show'] == "":
        passw_entry['show'] = "●"
        B1_show['text'] = '○'
        B1_show.update()
    passw_entry.update()

m = tk.Tk()
m.geometry('1920x1080')
m.title('Welcome')
m.configure(bg='black')

tk.Label(
    m,
    text='TIMETABLE MANAGEMENT SYSTEM',
    font=('Arial', 15, 'bold'),
    fg='white',
    bg='black'
).pack(pady=20)

tk.Label(
    m,
    text='Welcome!\nLogin to continue',
    font=('Arial', 12, 'italic'),
    fg='yellow',
    bg='black'
).pack(pady=10)

tk.Label(
    m,
    text='Username:',
    font=('Arial', 15),
    fg='white',
    bg='black'
).pack()

id_entry = tk.Entry(
    m,
    font=('Arial', 12),
    width=20,justify='left'
)
id_entry.pack(pady=5, ipady=3)

tk.Label(
    m,
    text='Password:',
    font=('Arial', 15),
    fg='white',
    bg='black',justify='left',
).pack()

pass_entry_f = tk.Frame(m, bg='black')
pass_entry_f.pack(pady=0)

passw_entry = tk.Entry(
    pass_entry_f,
    font=('Arial', 12),
    width=14,justify='left',
    show="●"
)
passw_entry.pack(side=tk.LEFT)

B1_show = tk.Button(
    pass_entry_f,
    text='○',
    font=('Arial', 12, 'bold'),
    command=show_passw,
    padx=5,
    bg='yellow',
    fg='black'
)
B1_show.pack(side=tk.RIGHT, padx=10)

combo1 = ttk.Combobox(
    m,
    values=['Student', 'Faculty', 'Admin'],
    font=('Arial', 11),justify='center',
)
combo1.pack(pady=10)
combo1.current(0)

tk.Button(
    m,
    text='Login',
    font=('Arial', 12, 'bold'),
    padx=30,
    command=challenge,
    bg='green',
    fg='white',
).pack(pady=(20, 10))  

m.mainloop()