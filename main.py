import os 
import re
import git
import time
from datetime import datetime
import sqlite3
import socket
import pymongo
import threading
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


error = 0
otpl =[]
new_email_list = []

func_list = ['dashboard']

def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        # Attempt to connect to a well-known DNS server (Google)
        socket.setdefaulttimeout(timeout)
        with socket.create_connection((host, port)):
            return True
    except OSError:
        return False

def update_day_date_time():
    now = datetime.now()
    
    day = now.strftime("%A") 
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    day_label.config(text=day)
    date_time_label.config(text=date_time)

    win.after(1000, update_day_date_time)


def get_percentage_of_day():
    now = datetime.now()
    seconds_passed = now.hour * 3600 + now.minute * 60 + now.second
    total_seconds_in_day = 24 * 3600
    # print(now.day())
    return (seconds_passed / total_seconds_in_day) * 100

def update_progress():
    percentage = get_percentage_of_day()
    # progress_var.set(percentage)
    daily_progress.set(get_percentage_of_day() / 100) 
    daily_progress_label.configure(text=f"{percentage:.2f}% day completed")
    win.after(1000, update_progress)

def generate_otp():
    return random.randint(100000, 999999)

week = {
    'Monday':1,
    'Tuesday':2,
    'Wednesday':3,
    'Thursday':4,
    'Friday':5,
    'Saturday':6,
    'Sunday':7
}

def get_fraction_of_week():
    global week
    
    now = datetime.now()
    day = now.strftime("%A") 
    
    day_count = week[day]
    
    weekly_progress_label.config(text = day)

    return (day_count/7)*100

def update_week_progress():
    
    day_frac = get_fraction_of_week()    

    weekly_progress.set(day_frac/100)
    
    win.after(1000, update_week_progress)
    
    
def get_monthly_percent():

    date = datetime.today().day

    monthly_progress_label.config (text=f"Day {date} of 30/31")
    
    return (date/30)*100

def update_month_progress():
    month_frac = get_monthly_percent()

    monthly_progress.set(month_frac/100)

    win.after(1000, update_month_progress)
    
def update_server(dictonary):
    global client_info
    
    client_info.insert_one(dictonary)
    messagebox.showinfo('Verification Done', 'Sign Up Successful!')    
    
    
def check_server(chk_value, updt_value):
    global client_info
    
    find_val = client_info.find({}, {'name':chk_value}, )
    

def send_otp(email):
    global current_dir
    if check_internet():
        otp = generate_otp()
        otpl.insert(0,otp)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        envars = current_dir/ ".env" # create .env file in current folder

        load_dotenv(envars)

        sender_email = os.getenv('EMAIL') #add your email in .env file
        sender_key = os.getenv('KEY') # add gamil app passwords in .env file

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
    global client_info, new_email_list
    if len(username.get().strip())<4:
        messagebox.showerror('Reset Password', f"No username found with '{username.get()}'")
    else:
        find_val_username = client_info.find_one(
                {"username":username.get().strip() })
        if find_val_username:
            contentframe.pack_forget()
            pass_reset_frame.pack()
            find_email = client_info.find_one({'username':username.get().strip()}, {'email':1})
            new_email = find_email['email']
            new_email_list.insert(0, new_email)
            
            threading.Thread(target=send_otp, args=(new_email,), daemon=True).start()
            reset_canvas.create_text(1000, 350, text=f'OTP sent on {new_email}', font=('Poppins', 20), fill='#6F6F6F' )
            # print(email)
        else:
            messagebox.showerror('Reset Password', f"No username found with '{username.get()}'")

def sign_up():
    contentframe.pack_forget()
    sign_up_frame.pack()
    # sign_up_canvas.pack()

def try_login ():
    
    if check_internet():
        
        username_value = username.get().strip()
        password_value = password.get()
        
        client_info_dict = {
                'username':username_value,
                'password':password_value,
            }
            
        find_val_username = client_info.find_one(
                {"username": client_info_dict["username"]})
        
        if 0 == 0 : #find_val_username:
            find_val_password = client_info.find_one(
                {"password": client_info_dict["password"]})
            if 0 == 0 : #find_val_password:
                contentframe.pack_forget()
                dashboard_frame.pack()
                username_label.config(text= username_value)
                update_day_date_time()
                update_progress()
                update_week_progress()
                update_month_progress()
                print(username_value,'\n',password_value)
            else:
                messagebox.showerror('Login Error', 'passowrd is wrong!')
        else:
            messagebox.showerror('Login Error', 'username is wrong!')
    else:
        messagebox.showerror('Connection Error', 'Please Check your internet connection!')

def reset_verify_otp():
    global otpl
    reset_otp_val = resetEmailotp.get()

    if str(otpl[0]) == reset_otp_val:
        pass_reset_frame.pack_forget()
        new_pass_frame.pack()
    else:
        messagebox.showerror('Verification Error', 'incorrect OTP, please resend the otp and enter the correct one!')

def reset_password():
    global client_info
    
    new_pass_update = client_info.update_one({'username': username.get().strip()}, {"$set":{'password':resetpass.get()}})

    if new_pass_update.matched_count>0:
        messagebox.showinfo('Password Reset', f'Your new password is {resetpass.get()}')
        new_pass_frame.pack_forget()
        contentframe.pack()

def reset_resend_otp():
    global new_email_list
    threading.Thread(target=send_otp, args=(new_email_list[0],), daemon=True).start()

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
        threading.Thread(target=send_otp, args=(email_value_signup,), daemon=True).start()
    else:
        error = 0
        messagebox.showerror('Recheck', 'Please recheck your credentials!')
            
    
def verify_otp():
    global otpl, client_info
    
    if email_otp.get() == str(otpl[0]):
        
        client_info_dict = {
            'username':username_signup.get().strip(),
            'password':password_signup.get(),
            'email':email_signup.get().strip(),
            'phone':int(phone_signup.get().strip())
        }
        
        find_val = client_info.find_one({
            "$or": [
                {"username": client_info_dict["username"]},
                {"phone": client_info_dict["phone"]},
                {"email": client_info_dict["email"]}
            ]
        })
        
        if find_val:
            messagebox.showerror('', 'username/phone/email already exist. Please Retry!')
        else:
            update_server(client_info_dict)
        
        
    else:
        messagebox.showerror('Verification Error', 'incorrect OTP, please resend the otp and enter the correct one!')


def resend_otp():
    threading.Thread(target=send_otp, args=(email_signup.get(),), daemon=True).start()
        
def get_back():
    verification_frame.pack_forget()
    sign_up_frame.pack()

def func_finder(prev_func_name):
    if prev_func_name == 'dashboard':
        dashboard_display.pack_forget()
    elif prev_func_name == 'inventory':
        inventory_display.pack_forget()
    elif prev_func_name == 'alert':
        alert_display.pack_forget()
    elif prev_func_name == 'billing':
        billing_display.pack_forget()
    elif prev_func_name == 'supplier':
        supply_display.pack_forget()
    elif prev_func_name == 'history':
        history_display.pack_forget()
    elif prev_func_name == 'setting':
        setting_display.pack_forget()
    elif prev_func_name == 'cc':
        cc_display.pack_forget()
    
    
def dashboardFunction():
    global func_list, func_name_dict
    prev_func_name = func_list[0]
    current_func_name = "dashboard"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        dashboard_display.pack(side='left')


def inventoryFunction():
    global func_list, func_name_dict
    prev_func_name = func_list[0]
    current_func_name = "inventory"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        inventory_display.pack(side='left')

def alertFunction():
    global func_list, func_name_dict
    prev_func_name = func_list[0]
    current_func_name = "alert"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        alert_display.pack(side='left')

def billingFunction():
    global func_list, func_name_dict
    prev_func_name = func_list[0]
    current_func_name = "billing"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        billing_display.pack(side='left')

def supplierFunction():
    global func_list, func_name_dict
    prev_func_name = func_list[0]
    current_func_name = "supplier"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        supply_display.pack(side='left')

def historyFunction():
    global func_list, func_name_dict
    prev_func_name = func_list[0]
    current_func_name = "history"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        history_display.pack(side='left')

def settingFunction():
    global func_list, func_name_dict
    prev_func_name = func_list[0]
    current_func_name = "setting"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        setting_display.pack(side='left')

def ccFunction():
    global func_list, func_name_dict
    prev_func_name = func_list[0]
    current_func_name = "cc"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        cc_display.pack(side='left')

if check_internet():
    current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
    envars_db = current_dir/ ".env" # create .env file in current folder

    load_dotenv(envars_db)

    client = pymongo.MongoClient(os.getenv('URL_Mongo'))

    login_signup_database = client['Login-Signup']
    client_info = login_signup_database.clien_infos
    
    win=Tk()
    win.geometry("1400x770+50+0")
    win.title("Bazaro")
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

    # =======================<<<<<<<<<<<< forget password INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================

    pass_reset_frame=Frame(win,height=770,width=1400,bg='red')
    pass_reset_frame.propagate(False)
    # pass_reset_frame.pack()


    reset_canvas=Canvas(pass_reset_frame,height=770,width=1400,bg='black',bd=0,highlightthickness=0, relief='ridge')
    reset_canvas.propagate(False)
    reset_canvas.pack()
    
    imagepath_1=cwd+"\\uiux\\forget_pass.png"
    openphoto_1=Image.open(imagepath_1).resize((1400,770))
    bgimage_1=ImageTk.PhotoImage(openphoto_1)
    reset_canvas.create_image(700,385, image=bgimage_1)
    
    resetEmailotp = StringVar()
    reset_email_otp = ctk.CTkEntry(reset_canvas, height=40,width=330, fg_color='#f2f3f4', text_color='black',
                                border_color='#FF8A00', bg_color='white', corner_radius=20, font=('Poppins', 22),
                                textvariable= resetEmailotp)
    reset_email_otp.place(x = 900, y = 400)
    
    reset_verify_button = ctk.CTkButton(reset_canvas, text="Verify", font=('Poppins', 26, 'bold'), height=45, width = 40, cursor='hand2',
                                fg_color='orange', bg_color='white', text_color='white', hover_color='black',
                                corner_radius=10, command = reset_verify_otp)
    reset_verify_button.place(x = 900, y = 480)

    resend_button = ctk.CTkButton(reset_canvas, text="Resend", font=('Poppins', 26, 'bold'), height=45, width = 40, cursor='hand2',
                                fg_color='orange', bg_color='white', text_color='white', hover_color='black',
                                corner_radius=10, command= reset_resend_otp)
    resend_button.place(x = 1020, y = 480)
    
    # =======================<<<<<<<<<<<< new password INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================

    new_pass_frame=Frame(win,height=770,width=1400,bg='red')
    new_pass_frame.propagate(False)

    new_pass_canvas=Canvas(new_pass_frame,height=770,width=1400,bg='black',bd=0,highlightthickness=0, relief='ridge')
    new_pass_canvas.propagate(False)
    new_pass_canvas.pack()
    
    imagepath_2=cwd+"\\uiux\\new_pass.png"
    openphoto_2=Image.open(imagepath_2).resize((1400,770))
    bgimage_2=ImageTk.PhotoImage(openphoto_2)
    new_pass_canvas.create_image(700,385, image=bgimage_2)
    
    resetpass = StringVar()
    reset_password_entry = ctk.CTkEntry(new_pass_canvas, height=40,width=330, fg_color='#f2f3f4', text_color='black',
                                border_color='#FF8A00', bg_color='white', corner_radius=20, font=('Poppins', 22),
                                textvariable= resetpass)
    reset_password_entry.place(x = 970, y = 400)
    
    reset_password_button = ctk.CTkButton(new_pass_canvas, text="Reset", font=('Poppins', 26, 'bold'), height=45, width = 40, cursor='hand2',
                                fg_color='orange', bg_color='white', text_color='white', hover_color='black',
                                corner_radius=10, command = reset_password)
    reset_password_button.place(x = 950, y = 480)
    
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

    imagepath4=cwd+"\\uiux\\verification2.png"
    openphoto4=Image.open(imagepath4).resize((1400,770))
    bgimage4=ImageTk.PhotoImage(openphoto4)
    verification_canvas.create_image(700,385, image=bgimage4)

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
    
    back_button = ctk.CTkButton(verification_frame, text="Back", font=('Poppins', 26, 'bold'), height=45, width = 40, cursor='hand2',
                                fg_color='orange', bg_color='white', text_color='white', hover_color='black',
                                corner_radius=10, command = get_back)
    back_button.place(x = 840, y = 510)

    verify_button = ctk.CTkButton(verification_frame, text="Verify", font=('Poppins', 26, 'bold'), height=45, width = 40, cursor='hand2',
                                fg_color='orange', bg_color='white', text_color='white', hover_color='black',
                                corner_radius=10, command = verify_otp)
    verify_button.place(x = 950, y = 510)

    resend_button = ctk.CTkButton(verification_frame, text="Resend", font=('Poppins', 26, 'bold'), height=45, width = 40, cursor='hand2',
                                fg_color='orange', bg_color='white', text_color='white', hover_color='black',
                                corner_radius=10, command= resend_otp)
    resend_button.place(x = 1070, y = 510)
    
    # =======================<<<<<<<<<<<< Dashboard INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================

    file_path = 'shopname.txt'
    shop_name = ''
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip().split()

            for parts in content:
                shop_name = shop_name+'-'+parts
            
    except FileNotFoundError:
        messagebox.showerror('File Error',f"The file '{file_path}' was not found.")
    except IOError:
        messagebox.showerror('Read Error',f"An error occurred while reading the file '{file_path}'.")

    r_shop_name = shop_name[1:]
    
    

    dashboard_frame=Frame(win,height=770,width=1400,bg='red')
    dashboard_frame.propagate(False)
    # dashboard_frame.pack()
    
    menu_frame=Frame(dashboard_frame,height=770,width=250,bg='red')
    menu_frame.propagate(False)
    menu_frame.pack(side='left')

    menu_canvas=Canvas(menu_frame,height=770,width=250,bg='blue',bd=0,highlightthickness=0, relief='ridge')
    menu_canvas.propagate(False)
    menu_canvas.pack()
    
    imagepath2=cwd+"\\uiux\\sidebar2.png"
    openphoto2=Image.open(imagepath2).resize((250,770))
    bgimage2=ImageTk.PhotoImage(openphoto2)
    menu_canvas.create_image(125,385, image=bgimage2)

    dashboard_button = ctk.CTkButton(menu_frame, text="DASHBOARD", font=('Poppins', 20), height=45, width = 170, cursor='hand2',
                                fg_color='#4B54F8', bg_color='#4B54F8', text_color='white', hover_color='#0713FF',
                                corner_radius=10, anchor='w', command= dashboardFunction )
    dashboard_button.place(x = 60, y = 100)
    
    inventory_button = ctk.CTkButton(menu_frame, text="INVENTORY", font=('Poppins', 20), height=45, width = 170, cursor='hand2',
                                fg_color='#4B54F8', bg_color='#4B54F8', text_color='white', hover_color='#0713FF',
                                corner_radius=10, anchor='w', command= inventoryFunction )
    inventory_button.place(x = 60, y = 175)
    
    alert_button = ctk.CTkButton(menu_frame, text="ALERTS", font=('Poppins', 20), height=45, width = 170, cursor='hand2',
                                fg_color='#4B54F8', bg_color='#4B54F8', text_color='white', hover_color='#0713FF',
                                corner_radius=10, anchor='w', command =alertFunction )
    alert_button.place(x = 60, y = 250)
    
    billing_button = ctk.CTkButton(menu_frame, text="Billings", font=('Poppins', 20), height=45, width = 170, cursor='hand2',
                                fg_color='#4B54F8', bg_color='#4B54F8', text_color='white', hover_color='#0713FF',
                                corner_radius=10, anchor='w', command = billingFunction )
    billing_button.place(x = 60, y = 325)
    
    suplier_button = ctk.CTkButton(menu_frame, text="SUPPLIER", font=('Poppins', 20), height=45, width = 170, cursor='hand2',
                                fg_color='#4B54F8', bg_color='#4B54F8', text_color='white', hover_color='#0713FF',
                                corner_radius=10, anchor='w', command= supplierFunction )
    suplier_button.place(x = 60, y = 395)
    
    history_button = ctk.CTkButton(menu_frame, text="HISTORY", font=('Poppins', 20), height=45, width = 170, cursor='hand2',
                                fg_color='#4B54F8', bg_color='#4B54F8', text_color='white', hover_color='#0713FF',
                                corner_radius=10, anchor='w', command= historyFunction )
    history_button.place(x = 60, y = 475)
    
    
    settings_button = ctk.CTkButton(menu_frame, text="Settings", font=('Poppins', 20), height=45, width = 170, cursor='hand2',
                                fg_color='#4B54F8', bg_color='#4B54F8', text_color='white', hover_color='#0713FF',
                                corner_radius=10, anchor='w', command= settingFunction )
    settings_button.place(x = 60, y = 560)
    
    cc_button = ctk.CTkButton(menu_frame, text="Customer Care", font=('Poppins', 20), height=45, width = 170, cursor='hand2',
                                fg_color='#4B54F8', bg_color='#4B54F8', text_color='white', hover_color='#0713FF',
                                corner_radius=10, anchor='w', command= ccFunction )
    cc_button.place(x = 60, y = 640)
    
    exit_button = ctk.CTkButton(menu_frame, text="Exit", font=('Poppins', 20), height=45, width = 170, cursor='hand2',
                                fg_color='#4B54F8', bg_color='#4B54F8', text_color='white', hover_color='#0713FF',
                                corner_radius=10, anchor='w' )
    exit_button.place(x = 60, y = 715)
    
    
    # =======================<<<<<<<<<<<< Dashboard Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================

    dashboard_display=Frame(dashboard_frame,height=770,width=1150,bg='blue')
    dashboard_display.propagate(False)
    dashboard_display.pack(side='left')
    
    dashboard_canvas=Canvas(dashboard_display,height=770,width=1150,bg='blue',bd=0,highlightthickness=0, relief='ridge')
    dashboard_canvas.propagate(False)
    dashboard_canvas.pack()


    imagepath3=cwd+"\\uiux\\dashboard2.png"
    openphoto3=Image.open(imagepath3).resize((1150,770))
    bgimage3=ImageTk.PhotoImage(openphoto3)
    dashboard_canvas.create_image(575,385, image=bgimage3)
    
    
    username_label = Label(dashboard_display, text='', font=('Poppins', 20), fg="black", bg = 'white')
    username_label.place(x = 100, y = 25)
    
    day_label = Label(dashboard_display, text='Tuesday', font = ('Poppins', 15), fg="#6F6F6F", bg='white')
    day_label.place(x = 1000, y = 10 )

    date_time_label =  Label(dashboard_display, text='20-05-2024 19:34', font = ('Poppins', 15), fg=  "black", bg='white')
    date_time_label.place(x = 915, y = 35)
    
    # progress_var = ctk.BooleanVar()
    daily_income_profit = ctk.CTkLabel(dashboard_display, text='Rs.400', font = ('poppins', 20, 'bold'), text_color="green",
                                       fg_color="white")
    daily_income_profit.place( x = 350, y = 160)
    
    daily_progress = ctk.CTkProgressBar(dashboard_display, orientation="horizontal", bg_color='white',
                                        width=300, progress_color="#4B54F8") # Initial set (0-1 scale)
    daily_progress.place( x = 35, y = 200)
    
    daily_progress_label = Label(dashboard_display, text='',font = ('Poppins', 12), fg="#6F6F6F", bg='white' )
    daily_progress_label.place(x = 340, y = 190)
    
    
    weekly_income_profit = ctk.CTkLabel(dashboard_display, text='Rs.5400', font = ('poppins', 20, 'bold'), text_color="green",
                                       fg_color="white")
    weekly_income_profit.place( x = 350, y = 225)
    
    weekly_progress = ctk.CTkProgressBar(dashboard_display, orientation="horizontal", bg_color='white',
                                        width=300, progress_color="#4B54F8")
    
    weekly_progress.place( x = 35, y = 270)
    
    weekly_progress_label = Label(dashboard_display, text='',font = ('Poppins', 12), fg="#6F6F6F", bg='white' )
    weekly_progress_label.place(x = 345, y = 260)
    
    monthly_income_profit = ctk.CTkLabel(dashboard_display, text='Rs.55400', font = ('poppins', 20, 'bold'), text_color="green",
                                       fg_color="white")
    monthly_income_profit.place( x = 350, y = 295)
    
    monthly_progress = ctk.CTkProgressBar(dashboard_display, orientation="horizontal", bg_color='white',
                                        width=300, progress_color="#4B54F8")
        
    monthly_progress.place( x = 35, y = 340 )
    
    monthly_progress_label = Label(dashboard_display, text='',font = ('Poppins', 12), fg="#6F6F6F", bg='white' )
    monthly_progress_label.place(x = 340, y = 330)
    
    # =======================<<<<<<<<<<<< Inventory Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================

    inventory_display=Frame(dashboard_frame,height=770,width=1150,bg='blue')
    inventory_display.propagate(False)
    inventory_display.pack(side='left')

    # =======================<<<<<<<<<<<< alert Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================

    alert_display=Frame(dashboard_frame,height=770,width=1150,bg='green')
    alert_display.propagate(False)
    alert_display.pack(side='left')
    
    # =======================<<<<<<<<<<<< billing Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================
    
    billing_display=Frame(dashboard_frame,height=770,width=1150,bg='yellow')
    billing_display.propagate(False)
    billing_display.pack(side='left')
    
    # =======================<<<<<<<<<<<< supply Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================
    
    supply_display=Frame(dashboard_frame,height=770,width=1150,bg='pink')
    supply_display.propagate(False)
    supply_display.pack(side='left')
    
    # =======================<<<<<<<<<<<< history Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================
    
    history_display=Frame(dashboard_frame,height=770,width=1150,bg='violet')
    history_display.propagate(False)
    history_display.pack(side='left')
    
    # =======================<<<<<<<<<<<< setting Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================
    
    setting_display=Frame(dashboard_frame,height=770,width=1150,bg='brown')
    setting_display.propagate(False)
    setting_display.pack(side='left')
    
    # =======================<<<<<<<<<<<< cc Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================
    
    cc_display=Frame(dashboard_frame,height=770,width=1150,bg='grey')
    cc_display.propagate(False)
    cc_display.pack(side='left')
    
    

    win.mainloop()
    
else:
    messagebox.showerror('Connection Error', 'Please Check your internet connection!')


