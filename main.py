import os 
import re
import sqlite3
import socket
from tkinter import*
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv


def generate_otp():
    return random.randint(100000, 999999)

# otp = generate_otp()

# print(f"Your 6-digit OTP is: {otp}")

def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        # Attempt to connect to a well-known DNS server (Google)
        socket.setdefaulttimeout(timeout)
        with socket.create_connection((host, port)):
            return True
    except OSError:
        return False
otpl =[]

def send_otp(email):
    
    if check_internet():
        otp = generate_otp()
        otpl.insert(0,otp)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
        envars = current_dir/ ".env"

        load_dotenv(envars)

        sender_email = os.getenv('EMAIL')
        sender_key = os.getenv('KEY')

        server.login(sender_email, sender_key)
        to_mail = email

        msg = EmailMessage()

        msg['Subject'] = 'OTP verification'
        msg['From'] = 'ytgamings802212@gmail.com'
        msg['to'] = to_mail

        msg.set_content("Your OTP is " + str(otp))
        server.send_message(msg)
        messagebox.showinfo('OTP send', 'OTP send!')
    else:
        messagebox.showerror('Connection Error', 'Please Check your internet connection!')

def new_password():
    pass

def sign_up():
    contentframe.pack_forget()
    sign_up_frame.pack()
    # sign_up_canvas.pack()

def try_login ():
    username_value = username.get()
    password_value = password.get()
    
    contentframe.pack_forget()

    print(username_value,'\n',password_value)

error = 0

def try_signup():
    global error
    username_value_signup =  username_signup.get().strip()
    email_value_signup = email_signup.get()
    phone_value_signup = phone_signup.get()
    password_value_signup = password_signup.get()
    
    if len(username_value_signup)<=2:
        messagebox.showerror('Incorrect Name', "Please enter your correct name!")
        error = error+1
    elif len(password_value_signup)<=4:
        messagebox.showwarning('Security Alert', 'Password length should atlest be 4')
        error = error+1
    else:
        pass
    
    
    email_condition = "^[a-z]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$"

    if re.search(email_condition, email_value_signup):
        pass
    else:
        error = error+1
        messagebox.showerror('Wrong Email Format', f"'{email_value_signup}' has a wrong email format, Please check again!")

    mobile_condition = "^\d{10}$"

    if re.search(mobile_condition, phone_value_signup):
        pass
    else:
        error = error+1
        messagebox.showerror('Wrong Phone Format', f"'{phone_value_signup}' is wrong phone format!")

    if error == 0:
        sign_up_frame.pack_forget()
        verification_frame.pack()
        send_otp(email_value_signup)
    else:
        error = 0
        messagebox.showerror('Recheck', 'Please recheck your credentials!')
            
    
def verify_otp():
    global otpl
    
    if email_otp.get() == str(otpl[0]):
        messagebox.showinfo('Verification Done', 'Sign Up Successful!')
    else:
        messagebox.showerror('Verification Error', 'incorrect OTP, please resend the otp and enter the correct one!')


def resend_otp():
    send_otp(email_signup.get())
        
    
        



win=Tk()
win.geometry("1400x770+50+0")
win.title("Contact Book")
# win.iconbitmap('logo.ico')

# =======================<<<<<<<<<<<< LOGIN INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================

contentframe=Frame(win,height=770,width=1400,bg='red')
contentframe.propagate(False)
contentframe.pack()


login_canvas=Canvas(contentframe,height=770,width=1400,bg='black',bd=0,highlightthickness=0, relief='ridge')
login_canvas.propagate(False)
login_canvas.pack()

cwd = os.getcwd()

imagepath=cwd+"\\uiux\\login 2.png"
openphoto=Image.open(imagepath).resize((1400,770))
bgimage=ImageTk.PhotoImage(openphoto)
login_canvas.create_image(700,385, image=bgimage)

username = StringVar()

username_entry = ctk.CTkEntry(login_canvas, height=40,width=330, fg_color='#f2f3f4', text_color='black',
                              border_color='#FF8A00', bg_color='white', corner_radius=20, font=('Poppins', 22),
                              textvariable= username)
username_entry.place(x = 600, y = 435)

password = StringVar()

password_entry = ctk.CTkEntry(login_canvas, height=40,width=330, fg_color='#f2f3f4', text_color='black',
                              border_color='#FF8A00', bg_color='white', corner_radius=20, font=('Poppins', 22),
                              textvariable= password)
password_entry.place(x = 600, y = 565)

pass_forget_button = ctk.CTkButton(login_canvas, text="Forgot password?", font=('arial', 12), height=1, width = 20, cursor='hand2',
                            fg_color='white', bg_color='white', text_color='#FF8A00', hover_color='white', command = new_password)
pass_forget_button.place(x = 400, y = 620)

new_member_button = ctk.CTkButton(login_canvas, text="New to Bazaro? Sign up!", font=('arial', 12), height=1, width = 20, cursor='hand2',
                            fg_color='white', bg_color='white', text_color='blue', hover_color='white', command=sign_up)
new_member_button.place(x = 860, y = 620)


continue_button = ctk.CTkButton(login_canvas, text="Continue", font=('arial', 26, 'bold'), height=45, width = 40, cursor='hand2',
                            fg_color='orange', bg_color='white', text_color='white', hover_color='black', corner_radius=10,
                            command=try_login)
continue_button.place(x = 635, y = 660)


# =======================<<<<<<<<<<<< SIGNUP INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================

sign_up_frame=Frame(win,height=770,width=1400,bg='blue')
sign_up_frame.propagate(False)
# sign_up_frame.pack()

sign_up_canvas=Canvas(sign_up_frame,height=770,width=1400,bg='blue',bd=0,highlightthickness=0, relief='ridge')
sign_up_canvas.propagate(False)
sign_up_canvas.pack()

cwd = os.getcwd()

imagepath1=cwd+"\\uiux\\sign up 2.png"
openphoto1=Image.open(imagepath1).resize((1400,770))
bgimage1=ImageTk.PhotoImage(openphoto1)
sign_up_canvas.create_image(700,385, image=bgimage1)


username_signup = StringVar()

username_entry_signup = ctk.CTkEntry(sign_up_frame, height=40,width=330, fg_color='#f2f3f4', text_color='black',
                              border_color='#FF8A00', bg_color='white', corner_radius=20, font=('Poppins', 22),
                              textvariable= username_signup)
username_entry_signup.place(x = 900, y = 145)

email_signup = StringVar()

email_entry_signup = ctk.CTkEntry(sign_up_frame, height=40,width=330, fg_color='#f2f3f4', text_color='black',
                              border_color='#FF8A00', bg_color='white', corner_radius=20, font=('Poppins', 22),
                              textvariable= email_signup)
email_entry_signup.place(x = 900, y = 225)

phone_signup = StringVar()

mobile_entry_signup = ctk.CTkEntry(sign_up_frame, height=40,width=330, fg_color='#f2f3f4', text_color='black',
                              border_color='#FF8A00', bg_color='white', corner_radius=20, font=('Poppins', 22),
                              textvariable= phone_signup)
mobile_entry_signup.place(x = 900, y = 315)

password_signup = StringVar()

password_entry_signup = ctk.CTkEntry(sign_up_frame, height=40,width=330, fg_color='#f2f3f4', text_color='black',
                              border_color='#FF8A00', bg_color='white', corner_radius=20, font=('Poppins', 22),
                              textvariable= password_signup)
password_entry_signup.place(x = 900, y = 405)


letsgo_button = ctk.CTkButton(sign_up_frame, text="Lets go!", font=('arial', 26, 'bold'), height=45, width = 40, cursor='hand2',
                            fg_color='orange', bg_color='white', text_color='white', hover_color='black', corner_radius=10,
                            command = try_signup)
letsgo_button.place(x = 950, y = 500)

# =======================<<<<<<<<<<<< Verification INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================

verification_frame=Frame(win,height=770,width=1400,bg='green')
verification_frame.propagate(False)
# sign_up_frame.pack()

verification_canvas=Canvas(verification_frame,height=770,width=1400,bg='blue',bd=0,highlightthickness=0, relief='ridge')
verification_canvas.propagate(False)
verification_canvas.pack()

imagepath2=cwd+"\\uiux\\verification2.png"
openphoto2=Image.open(imagepath2).resize((1400,770))
bgimage2=ImageTk.PhotoImage(openphoto2)
verification_canvas.create_image(700,385, image=bgimage2)

email_otp = StringVar()

email_otp_entry = ctk.CTkEntry(verification_frame, height=40,width=330, fg_color='#f2f3f4', text_color='black',
                              border_color='#FF8A00', bg_color='white', corner_radius=20, font=('Poppins', 22),
                              textvariable= email_otp)
email_otp_entry.place(x = 910, y = 300)

phone_otp = StringVar()

email_otp_entry = ctk.CTkEntry(verification_frame, height=40,width=330, fg_color='#f2f3f4', text_color='black',
                              border_color='#FF8A00', bg_color='white', corner_radius=20, font=('Poppins', 22),
                              textvariable= phone_otp)
email_otp_entry.place(x = 910, y = 430)

verify_button = ctk.CTkButton(verification_frame, text="Verify", font=('Poppins', 26, 'bold'), height=45, width = 40, cursor='hand2',
                            fg_color='orange', bg_color='white', text_color='white', hover_color='black',
                            corner_radius=10, command = verify_otp)
verify_button.place(x = 900, y = 510)

next_button = ctk.CTkButton(verification_frame, text="Resend", font=('Poppins', 26, 'bold'), height=45, width = 40, cursor='hand2',
                            fg_color='orange', bg_color='white', text_color='white', hover_color='black',
                            corner_radius=10, command= resend_otp)
next_button.place(x = 1020, y = 510)

win.mainloop()
