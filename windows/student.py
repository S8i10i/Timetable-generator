import re
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

fid = passw = conf_passw = name = roll = section = None


'''
    LIST OF FUNCTIONS USED FOR VARIOUS FUNCTIONS THROUGH TKinter INTERFACE
        * create_treeview()
        * update_treeview()
        * parse_data()
        * update data()
        * remove_data()
        * show_passw()
'''

# create treeview (call this function once)
def create_treeview():
    tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 6)))
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("#1", width=70, stretch=tk.NO)
    tree.column("#2", width=200, stretch=tk.NO)
    tree.column("#3", width=80, stretch=tk.NO)
    tree.column("#4", width=80, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('#1', text="sid")
    tree.heading('#2', text="Name")
    tree.heading('#3', text="Roll")
    tree.heading('#4', text="Batch")
    tree.heading('#5', text="Email")
    tree['height'] = 12


# update treeview (call this function after each update)
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT SID, NAME, ROLL, SECTION, EMAIL FROM STUDENT")
    for row in cursor:
        tree.insert(
            "",
            0,
            values=(row[0], row[1], row[2], row[3], row[4])
        )
    tree.place(x=530, y=100)

def validate(value):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(pattern, value) is None:
        return False
    else:
        return True
    
def password_check(passwd):     
    SpecialSym =['$', '@', '#', '%', '*']
    val = True
        
    if len(passwd) < 6:
        messagebox.showwarning("Bad Input",'password length should be at least 6')
        val = False
        return val
            
    if len(passwd) > 20:
        messagebox.showwarning("Bad Input",'password length should be not be greater than 20')
        val = False
        return val
            
    if not any(char.isdigit() for char in passwd):
        messagebox.showwarning("Bad Input",'Password should have at least one numeral')
        val = False
        return val
            
    if not any(char.isupper() for char in passwd):
        messagebox.showwarning("Bad Input",'Password should have at least one uppercase letter')
        val = False
        return val
            
    if not any(char.islower() for char in passwd):
        messagebox.showwarning("Bad Input",'Password should have at least one lowercase letter')
        val = False
        return val
            
    if not any(char in SpecialSym for char in passwd):
        messagebox.showwarning("Bad Input",'Password should have at least one of the symbols $@#*')
        val = False
        return val

# Parse and store data into database and treeview upon clcicking of the add button
def parse_data():
    fid = str(fid_entry.get())
    passw = str(passw_entry.get())
    conf_passw = str(conf_passw_entry.get())
    name = str(name_entry.get()).upper()
    roll = str(roll_entry.get())
    section = str(sec_entry.get()).upper()
    email=str(email_entry.get()).upper()
    if fid == "" or passw == "" or \
        conf_passw == "" or name == "" or \
        roll == "" or section == "":
        messagebox.showwarning("Bad Input", "Some fields are empty! Please fill them out!")
        return

    if password_check(passw)==False:
        return
    
    if passw != conf_passw:
        messagebox.showerror("Passwords mismatch", "Password and confirm password didnt match. Try again!")
        passw_entry.delete(0, tk.END)
        conf_passw_entry.delete(0, tk.END)
        return
    
    if validate(email)==False:
        messagebox.showerror("Bad Input","Email field is invalid")
        return

    conn.execute(f"REPLACE INTO STUDENT (SID, PASSW, NAME, ROLL, SECTION, EMAIL)\
        VALUES ('{fid}','{passw}','{name}', '{roll}', '{section}', '{email}')")
    conn.commit()
    update_treeview()
    
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    sec_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# update a row in the database
def update_data():
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    sec_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    # try:
    #     print(tree.selection())
    if len(tree.selection()) > 1:
        messagebox.showerror("Bad Select", "Select one student at a time to update!")
        return
    try:
        q_fid = tree.item(tree.selection()[0])['values'][0]
    except:
        messagebox.showerror("Bad Select", "Select at least one student at a time to update!")
        return
    cursor = conn.execute(f"SELECT * FROM STUDENT WHERE SID = '{q_fid}'")

    cursor = list(cursor)
    fid_entry.insert(0, cursor[0][0])
    passw_entry.insert(0, cursor[0][1])
    conf_passw_entry.insert(0, cursor[0][1])
    name_entry.insert(0, cursor[0][2])
    roll_entry.insert(0, cursor[0][3])
    sec_entry.insert(0, cursor[0][4])
    email_entry.insert(0, cursor[0][5])     
    conn.execute(f"DELETE FROM STUDENT WHERE SID = '{cursor[0][0]}'")
    conn.commit()
    
    update_treeview()
        
    #update_treeview()

    #except Exception as X:
        #messagebox.showerror("Bad Select", X)
        #return


# remove selected data from databse and treeview
def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a student from the list first!")
        return
    for i in tree.selection():
        # print(tree.item(i)['values'][0])
        conn.execute(f"DELETE FROM STUDENT WHERE SID = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()


# toggles between show/hide password
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




# main
if __name__ == "__main__":  

    '''
        DATABASE CONNECTIONS AND SETUP
    '''

    # connecting database
    conn = sqlite3.connect(r'files/timetable.db')

    # creating Tabe in the database
    conn.execute('CREATE TABLE IF NOT EXISTS STUDENT\
    (SID CHAR(10) NOT NULL PRIMARY KEY,\
    PASSW CHAR(50) NOT NULL,\
    NAME CHAR(50) NOT NULL,\
    ROLL INTEGER NOT NULL,\
    SECTION CHAR(5) NOT NULL,\
    EMAIL CHAR(50))')


    '''
        TKinter WINDOW SETUP WITH WIDGETS
            * Label(1-11)
            * Entry(6)
            * ComboBox(1-2)
            * Treeview(1)
            * Button(1-3)
    '''

    # TKinter Window
    subtk = tk.Tk()
    subtk.geometry('1200x550')
    subtk.config(background="black")
    subtk.title('Add/Update Students')

    # Label1
    tk.Label(
        subtk,
        text='LIST OF STUDENTS',
         fg='white',
        bg='black',
        font=('Consolas', 20, 'bold')
    ).place(x=700, y=50)

    # Label2
    tk.Label(
        subtk,
        text='ADD UPDATE STUDENTS',
         fg='white',
        bg='black',
        font=('Consolas', 20, 'bold')
    ).place(x=110, y=50)

    # Label3
    tk.Label(
        subtk,
        text='Add information in the following prompt!',
        fg='white',
        bg='black',
        font=('Consolas', 10, 'italic')
    ).place(x=110, y=85)

    # Label4
    tk.Label(
        subtk,
        text='Student id:',
        fg='white',
        bg='black',
        font=('Consolas', 12)
    ).place(x=100, y=130)

    # Entry1
    fid_entry = tk.Entry(
        subtk,
        font=('Consolas', 12),
        width=20
    )
    fid_entry.place(x=260, y=130)

    # Label5
    tk.Label(
        subtk,
        text='Password:',
        fg='white',
        bg='black',
        font=('Consolas', 12)
    ).place(x=100, y=170)

    # Entry2
    passw_entry = tk.Entry(
        subtk,
        font=('Consolas', 12),
        width=20,
        show="●"
    )
    passw_entry.place(x=260, y=170)

    B1_show = tk.Button(
        subtk,
        text='○',
        bg='yellow',
        font=('Consolas', 9, 'bold'),
        command=show_passw
    )
    B1_show.place(x=460,y=170)

    # Label6
    tk.Label(
        subtk,
        text='Confirm Password:',
        fg='white',
        bg='black',
        font=('Consolas', 12)
    ).place(x=100, y=210)

    # Entry3
    conf_passw_entry = tk.Entry(
        subtk,
        font=('Consolas', 12),
        width=20,
        show="●"
    )
    conf_passw_entry.place(x=260, y=210)

    # Label7
    tk.Label(
        subtk,
        text='Student Name:',
        fg='white',
        bg='black',
        font=('Consolas', 12)
    ).place(x=100, y=250)

    # Entry4
    name_entry = tk.Entry(
        subtk,
        font=('Consolas', 12),
        width=20,
    )
    name_entry.place(x=260, y=250)

    # Label8
    tk.Label(
        subtk,
        text='Roll no.:',
        fg='white',
        bg='black',
        font=('Consolas', 12)
    ).place(x=100, y=290)

    # Entry5
    roll_entry = tk.Entry(
        subtk,
        font=('Consolas', 12),
        width=10,
    )
    roll_entry.place(x=260, y=290)

    # Label9
    tk.Label(
        subtk,
        text='Batch:',
        fg='white',
        bg='black',
        font=('Consolas', 12)
    ).place(x=100, y=330)

    # Entry6
    sec_entry = tk.Entry(
        subtk,
        font=('Consolas', 12),
        width=10,
    )
    sec_entry.place(x=260, y=330)

    tk.Label(
        subtk,
        text='Email:',
        fg='white',
        bg='black',
        font=('Consolas', 12)
    ).place(x=100, y=370)

    email_entry = tk.Entry(
        subtk,
        font=('Consolas', 12),
        width=20,
    )
    email_entry.place(x=260, y=370)
    # Button1
    B1 = tk.Button(
        subtk,
        text='ADD STUDENT',
        fg='white',
        bg='green',
        font=('Consolas', 12),
        command=parse_data
    )
    B1.place(x=150,y=430)


    # Button2
    B2 = tk.Button(
        subtk,
        text='UPDATE STUDENT',
        fg='white',
        bg='green',
        font=('Consolas', 12),
        command=update_data
    )
    B2.place(x=410,y=430)

    # Treeview1
    tree = ttk.Treeview(subtk)
    create_treeview()
    update_treeview()

    # Button3
    B3 = tk.Button(
        subtk,
        text='DELETE STUDENT(s)',
        fg='white',
        bg='green',
        font=('Consolas', 12),
        command=remove_data
    )
    B3.place(x=650,y=430)

    # looping Tkiniter window
    subtk.mainloop()
    conn.close() # close database after all operations
