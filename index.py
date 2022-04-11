#import modules

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog 
import sqlite3 as sq
import os

# Designing window for registration

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("500x450")

    global username
    global Phone_number
    global Email_Id
    global password
    global username_entry
    global Phone_number_entry
    global Email_Id_entry
    global password_entry
    
    username = StringVar()
    Phone_number = StringVar()
    Email_Id = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter details below", bg="brown").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    Phone_number_lable = Label(register_screen, text="Phone_number * ")
    Phone_number_lable.pack()
    Phone_number_entry = Entry(register_screen, textvariable=Phone_number)
    Phone_number_entry.pack()
    Email_Id_lable = Label(register_screen, text="Email_Id * ")
    Email_Id_lable.pack()
    Email_Id_entry = Entry(register_screen, textvariable=Email_Id)
    Email_Id_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="green", command = register_user).pack()


# Designing window for login 

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()

# Implementing event on register button

def register_user():

    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()

# Implementing event on login button 

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()

        else:
            password_not_recognised()

    else:
        user_not_found()

# Designing popup for login success

def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("600x200")
    Label(login_success_screen, text="Login Success! You are welcome to our site").pack()
    Button(login_success_screen, text="Add Subjects", command=task).pack()
    Label(login_success_screen, text="Enter here").pack()
    Button(login_success_screen, text="Click Here", command=move_login_success).pack()
    
def task():
    root = tk.Tk()
    root.title('To-Do List')
    root.geometry("400x250+500+300")
    conn = sq.connect('todo.db')
    cur = conn.cursor()
    cur.execute('create table if not exists tasks (title text)')
    task = []
    #------------------------------- Functions--------------------------------
    def addTask():
        word = e1.get()
        if len(word)==0:
            messagebox.showinfo('Empty Entry', 'Enter task name')
        else:
            task.append(word)
            cur.execute('insert into tasks values (?)', (word,))
            listUpdate()
            e1.delete(0,'end')
    
    def listUpdate():
        clearList()
        for i in task:
            t.insert('end', i)
    
    def delOne():
        try:
            val = t.get(t.curselection())
            if val in task:
                task.remove(val)
                listUpdate()
                cur.execute('delete from tasks where title = ?', (val,))
        except:
                    messagebox.showinfo('Cannot Delete', 'No Task Item Selected')
        
    def deleteAll():
        mb = messagebox.askyesno('Delete All','Are you sure?')
        if mb==True:
            while(len(task)!=0):
                task.pop()
                cur.execute('delete from tasks')
                listUpdate()
    
    def clearList():
        t.delete(0,'end')
    
    def bye():
        print(task)
        root.destroy()
    
    def retrieveDB():
        while(len(task)!=0):
            task.pop()
            for row in cur.execute('select title from tasks'):
                task.append(row[0])
          
    #------------------------------- Functions--------------------------------
    
    l1 = ttk.Label(root, text = 'Add your subject to study')
    l2 = ttk.Label(root, text='Enter Subjects: ')
    e1 = ttk.Entry(root, width=21)
    t = tk.Listbox(root, height=11, selectmode='SINGLE')
    b1 = ttk.Button(root, text='Add Subject', width=20, command=addTask)
    b2 = ttk.Button(root, text='Delete', width=20, command=delOne)
    b3 = ttk.Button(root, text='Delete all', width=20, command=deleteAll)
    b4 = ttk.Button(root, text='Exit', width=20, command=bye)
    retrieveDB()
    listUpdate()
    #Place geometry
    l2.place(x=50, y=50)
    e1.place(x=50, y=80)
    b1.place(x=50, y=110)
    b2.place(x=50, y=140)
    b3.place(x=50, y=170)
    b4.place(x=50, y =200)
    l1.place(x=50, y=10)
    t.place(x=220, y =50)
    
    root.mainloop()
    conn.commit()
    cur.close()

# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found).pack()

# Deleting popups

def move_login_success():
    global move_login_success_screen
    move_login_success_screen = Toplevel(login_success_screen)
    move_login_success_screen.title("upload your notes in form of text")
    move_login_success_screen.geometry("450x200")
    Label(move_login_success_screen, text="upload your notes").pack()
    Button(move_login_success_screen, text="OK", command=upload_documents).pack()
    Label(move_login_success_screen, text="download your notes").pack()
    Button(move_login_success_screen, text="OK", command=download_documents).pack()
    Label(move_login_success_screen, text="Index").pack()
    Button(move_login_success_screen, text="OK", command=index1).pack()


def upload_documents():
    global upload_screen
    upload_screen = Toplevel(move_login_success_screen)
    upload_screen.title("click one of the following")
    upload_screen.geometry("300x250")
    Label(upload_screen, text="").pack()
    Button(upload_screen, text="Cse 205", command = upload).pack()
    Label(upload_screen, text="").pack()
    Button(upload_screen, text="INT 306", command=upload).pack()
    Label(upload_screen, text="").pack()
    Button(upload_screen, text="INT 213", command = upload).pack()
    Label(upload_screen, text="").pack()
    Button(upload_screen, text="CSE 320", command=upload).pack()

def upload():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.doc*"), ("all files", "*.*"))) 
    label_file_explorer.configure(text="File Opened: "+filename) 
    window = Tk() 
    window.title('File Explorer') 
    window.geometry("500x500")  
    window.config(background = "white")
    label_file_explorer = Label(window,text = "File Explorer using Tkinter", width = 100, height = 4, fg = "blue") 
    button_explore = Button(window, text = "Browse Files", command = browseFiles) 
    button_exit = Button(window,text = "Exit", command = exit) 
    label_file_explorer.grid(column = 1, row = 1) 
    button_explore.grid(column = 1, row = 2) 
    button_exit.grid(column = 1,row = 3) 
    window.mainloop() 

def download_documents():
    global download_screen
    download_screen = Toplevel(move_login_success_screen)
    download_screen.title("click one of the following")
    download_screen.geometry("300x250")
    Label(download_screen, text="").pack()
    Button(download_screen, text="Cse 205", command=download).pack()
    Label(download_screen, text="").pack()
    Button(download_screen, text="INT 306", command=download).pack()
    Label(download_screen, text="").pack()
    Button(download_screen, text="INT 213", command=download).pack()
    Label(download_screen, text="").pack()
    Button(download_screen, text="CSE 320", command=download).pack()
def download():
    main = Tk() 
    Lb = Listbox(main) 
    Lb.insert(1, 'Python') 
    Lb.insert(2, 'Java') 
    Lb.insert(3, 'C++') 
    Lb.insert(4, 'Any other') 
    Lb.pack() 
    main.mainloop( ) 
def index1():
    app = tk.Tk()
    OptionList = ["MTH 401","Logic and proof","Recurrsion","Relations","Graphs","Trees","Algorithms"]
    OptionList1 = ["CSE 401","Logic and proof","Recurrsion","Relations","Graphs","Trees","Algorithms"] 
    OptionList2 = ["CSE 401","Logic and proof","Recurrsion","Relations","Graphs","Trees","Algorithms"] 
    app.geometry('100x200')

    variable = tk.StringVar(app)
    variable.set(OptionList[0])

    opt = tk.OptionMenu(app, variable, *OptionList)
    opt.config(width=90, font=('Helvetica', 12))
    opt.pack()
    opt = tk.OptionMenu(app, variable, *OptionList1)
    opt.config(width=90, font=('Helvetica', 12))
    opt.pack()
    opt = tk.OptionMenu(app, variable, *OptionList2)
    opt.config(width=90, font=('Helvetica', 12))
    opt.pack()

    app.mainloop()
    
    
def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()

    main_screen.mainloop()
main_account_screen()
