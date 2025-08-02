from tkinter import *
from tkinter import messagebox
import db_connection


conn = db_connection.connect_to_db()

window = Tk()
window.title("Login form")
window.geometry('400x440')
window.configure(bg='#333333')




def login():
    username = username_entry.get()

    password = password_entry.get()
    
    role =  db_connection.validate_login(conn,username,password)
    
    if role == "admin":
        #messagebox.showinfo("Sucess","Welcome Admin")
        #print('admin')
        window.destroy()
        import admin_interface
        admin_interface.show_admin_gui()
    elif role == "user":
        #messagebox.showinfo("Sucess","Welcome Player")

        
        playerid = db_connection.player_name(conn,username,password)
        window.destroy()
        import user_interface
        user_interface.show_player_gui(playerid)
        
    else:
        messagebox.showerror("Error","Invalid Login")



def signup():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE role='admin'")
    if cur.fetchone() is not None:
        messagebox.showerror("Error","Admin already exists.")
        return
    
    signup_window = Toplevel()
    signup_window.title("Signup form")
    signup_window.geometry('400x440')
    signup_window.configure(bg='#333333')
    frame = Frame(signup_window, bg='#333333')
    signup_label = Label(
        frame, text="SignUp", bg='#333333', fg="#FF3399", font=("Arial", 30))
    username2_label = Label(
        frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    username2_entry = Entry(frame, font=("Arial", 16))
    password2_entry = Entry(frame, show="*", font=("Arial", 16))
    password2_label = Label(
        frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    

    def confirm_signup():
        username=username2_entry.get()
        password=password2_entry.get()
        cur.execute("INSERT INTO users(username,password,role)VALUES(%s, %s, 'admin')",(username, password))
        conn.commit()
        messagebox.showinfo("Success","Admin account created.")
        signup_window.destroy()
    signup2_button = Button (
        frame, text="SignUp", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16),command=confirm_signup )
    signup_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
    username2_label.grid(row=1, column=0)
    username2_entry.grid(row=1, column=1, pady=20)
    password2_label.grid(row=2, column=0)
    password2_entry.grid(row=2, column=1, pady=20)
    signup2_button.grid(row=3,column=1,sticky=E)
    frame.pack()
    

frame = Frame(bg='#333333')



login_label = Label(
    frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
username_label = Label(
    frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = Entry(frame, font=("Arial", 16))
password_entry = Entry(frame, show="*", font=("Arial", 16))
password_label = Label(
    frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_button = Button(
    frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)
signup_button = Button (
    frame, text="SignUp", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16),command=signup)

window.bind('<Return>', lambda event: login_button.invoke())


login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=1,pady=20,sticky=W)
signup_button.grid(row=3,column=1,sticky=E)

frame.pack()

window.mainloop()

