import os 
import re
import git
import time
import openpyxl
from datetime import datetime
import sqlite3
import socket
import pymongo
import os
import pythoncom
import win32com.client as win32
import threading
from tkinter import*
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkcalendar import Calendar
from PIL import Image, ImageTk
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
import random
import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd


error = 0
otpl =[]
new_email_list = []

func_list = ['dashboard']

inventory_func_list = ['None']

product_id_found = {
    'Update':False  ,
    'UID':000
}

choice_list = []


username_list = []

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
    global username_list
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
                username_list.insert(0, username_value)
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
    global inventory_func_list
    if prev_func_name == 'dashboard':
        dashboard_display.pack_forget()
    elif prev_func_name == 'inventory':
        inventory_display.pack_forget()
        if inventory_func_list[0] == 'add_stock':
            add_stock_frame.pack_forget()
        elif inventory_func_list[0] == 'update_stock':
            update_stock_frame.pack_forget()
        elif inventory_func_list[0] == 'analyse_stock':
            stock_analytics_frame.pack_forget()
        
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
    global func_list
    prev_func_name = func_list[0]
    current_func_name = "dashboard"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        dashboard_display.pack(side='left')


def inventoryFunction():
    global func_list
    prev_func_name = func_list[0]
    current_func_name = "inventory"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        inventory_display.pack(side='left')

def alertFunction():
    global func_list
    prev_func_name = func_list[0]
    current_func_name = "alert"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        alert_display.pack(side='left')

def billingFunction():
    global func_list
    prev_func_name = func_list[0]
    current_func_name = "billing"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        billing_display.pack(side='left')

def supplierFunction():
    global func_list
    prev_func_name = func_list[0]
    current_func_name = "supplier"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        supply_display.pack(side='left')

def historyFunction():
    global func_list
    prev_func_name = func_list[0]
    current_func_name = "history"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        history_display.pack(side='left')

def settingFunction():
    global func_list
    prev_func_name = func_list[0]
    current_func_name = "setting"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        setting_display.pack(side='left')

def ccFunction():
    global func_list
    prev_func_name = func_list[0]
    current_func_name = "cc"
    if prev_func_name == current_func_name:
        pass
    else:
        func_finder(prev_func_name)
        func_list.insert(0, current_func_name)
        cc_display.pack(side='left')

def stock_add():
    global inventory_func_list
    inventory_display.pack_forget()
    add_stock_frame.pack(side='left')
    
    inventory_func_list.insert(0, 'add_stock')

def update_stock():
    global inventory_func_list
    inventory_display.pack_forget()   
    update_stock_frame.pack(side='left')
    inventory_func_list.insert(0, 'update_stock')

def analyse_stock():
    global inventory_func_list
    inventory_display.pack_forget()   
    stock_analytics_frame.pack(side='left')
    inventory_func_list.insert(0, 'analyse_stock')
    fetch_and_display_inventory()

def open_calendar():
    top = Toplevel(win)
    top.title("Select a Date")
    top.geometry("300x300")

    cal = Calendar(top, selectmode='day', year=2025, month=5, day=22)
    cal.pack(pady=10)

    def grab_date():
        selected_date = cal.get_date()  # Format is typically mm/dd/yyyy
        date_obj = datetime.strptime(selected_date, "%m/%d/%y")  # Parse input
        formatted_date = date_obj.strftime("%d/%m/%Y")   
        mfdate.set(formatted_date)
        # date_label.configure(text=f"Date: {selected_date}")
        top.destroy()

    ctk.CTkButton(top, text="Select", command=grab_date).pack(pady=5)
    
def open_calendar1():
    top = Toplevel(win)
    top.title("Select a Date")
    top.geometry("300x300")

    cal = Calendar(top, selectmode='day', year=2025, month=5, day=22)
    cal.pack(pady=10)

    def grab_date():
        selected_date = cal.get_date()  # Format is typically mm/dd/yyyy
        date_obj = datetime.strptime(selected_date, "%m/%d/%y")  # Parse input
        formatted_date = date_obj.strftime("%d/%m/%Y")
        expdate.set(formatted_date)
        # date_label.configure(text=f"Date: {selected_date}")
        top.destroy()

    ctk.CTkButton(top, text="Select", command=grab_date).pack(pady=5)

def add_stock_to_dbs():
    global inventory
      
    find_product_id = inventory.find_one(
    {"Product_ID": barid.get()})
    
    find_product_name = inventory.find_one(
        {"Product_Name": productname.get().lower()}
    )
    
    if find_product_id or find_product_name:
        return "0"
    else:
        return "1"
        

def add_stock():
    global inventory
    if len(barid.get())>0:
        eligibility = add_stock_to_dbs()

        if eligibility is True:
            print("True")
        elif eligibility is False:
            print("False")
        else:
            if eligibility == '0':
                response = messagebox.askyesno("Confirm", "The Product with the given ID ot Name already exist. Do you want to update stock Quantity?")
                if response:
                    check_quantity = inventory.find_one({'Product_ID':barid.get()}, {'Quantity':1})
                    if check_quantity:
                        if check_quantity['Quantity'] == 0:
                            try:
                                if len(mfdate.get())>=4 and len(expdate.get())>= 4 and int(productqty.get()) > 0:
                                    product_dict_to_update = {
                                        'Quantity': int(productqty.get()),
                                        'Manufacture_Date': mfdate.get(),
                                        'Expire_Date': expdate.get()
                                    }
                                    
                                    inventory.update_one({'Product_ID':barid.get()}, {"$set":product_dict_to_update})
                                    messagebox.showinfo('Stock Update', f"Stock with ID {barid.get()} is updated!")
                                else:
                                    messagebox.showinfo('Stock Quantity Update', 'While updating the stock quantity, you need to re-enter Manufacture and Expire date and product quantity.')
                            except ValueError:
                                messagebox.showerror('')
                                
                        else:
                            messagebox.showinfo('Product Quantity', f"You can not add more stock as you have {str(check_quantity['Quantity'])} still left!Add when it is Zero!")
                    else:
                        messagebox.showerror('ID Error', 'Unexpected error occured!')
                else:
                    messagebox.showwarning("Duplication", "Product name or Product ID already exist!")
                    should_add = False
            else:
                should_add = True
                if len(productname.get())>0  and len(productqty.get())>0 and len(cp.get())>0 and len(sp.get())>0 and len(mfdate.get())>=4 and len(expdate.get())>= 4:
                    try:
                        if int(productqty.get()) < 0:
                            messagebox.showerror('Product Quantity','Invalid Product Quantity')
                            should_add = False
                        elif float(cp.get()) < 0:
                            messagebox.showerror('Cost Price','Invalid Cost Price!')
                            should_add = False
                        elif float(sp.get()) < 0:
                            messagebox.showerror('Selling Price','Invalid Selling Price!')
                            should_add = False
                    except ValueError:
                        messagebox.showerror('Input Error', 'Product Quantity must be an integer!\nor\nSP or CP must be Positive Number')
                        should_add = False
                else:
                    messagebox.showinfo('Empty Inputs', 'Entry fields must not be empty!')
                    should_add = False
                    
                if should_add is not False:      
                    should_add = True
                    if len(tax.get()) == 0:
                        taxs = float(0)
                    else:
                        try:    
                            taxs = float(tax.get())
                        except ValueError:
                            messagebox.showerror('Input Error','Tax Entry Should not contain alphabets or special Characters!')
                            should_add = False
        try:                
            if should_add is True:
                print("Entering This area")
                product_dict_to_add = {
                    'Product_ID': barid.get(),
                    'Product_Name': productname.get().lower(),
                    'Quantity': int(productqty.get()),
                    'Cost_Price': float(cp.get()),
                    'Selling_Price': float(sp.get()),
                    'Tax': taxs,
                    'Discount': 0.0,
                    'Manufacture_Date': mfdate.get(),
                    'Expire_Date': expdate.get()
                }
                # print(product_dict_to_add)
                inventory.insert_one(product_dict_to_add)
                messagebox.showinfo('Successfull', 'Product Added Successfully!')
            else:
                pass
        except UnboundLocalError:
            pass
    else:
        messagebox.showinfo('ID not found', 'Please Scan the product barcode!')
 
def clear_inventory_entries():
    bar_id_entry.delete(0, 'end')
    productname_entry.delete(0, 'end')
    productQuantity_entry.delete(0, 'end')
    cp_entry.delete(0, 'end')
    sp_entry.delete(0, 'end')
    tax_entry.delete(0, 'end')
    mf_date_entry.delete(0, 'end')
    exp_date_entry.delete(0, 'end')

def back_stock_entry():
    add_stock_frame.pack_forget()
    inventory_display.pack(side='left')
def back_update_entry():
    update_stock_frame.pack_forget()
    inventory_display.pack(side='left')
def analytics_back():
    stock_analytics_frame.pack_forget()
    inventory_display.pack(side='left')
    
def find_item_in_update():
    global product_id_found
    id_val = item_id_in_update.get()
    find_product = inventory.find_one(
        {"Product_ID": id_val}
    )
    try:
        if find_product:
            find_result_label.configure( text = f"Item Found:{find_product['Product_Name']}", fg ='White', bg ='#4B54F8', width=(len(find_product)+10) )
            find_result_label.place(x = 585, y = 180) #(x = 585, y = 118)
            product_id_found['Update'] = True
            product_id_found['UID'] = find_product['Product_ID']
        else:
            find_result_label.configure( text = "Item Not Found!",fg ='White', bg ='red', width=15)
            find_result_label.place(x = 585, y = 180)
            product_id_found['Update'] = False
            product_id_found['UID'] = find_product['Product_ID']
    except TypeError:
        pass

def update_product():
    global product_id_found
    should_update = product_id_found['Update']
    update_ID = product_id_found['UID']
    if should_update is True:
        try:
            if len(newproductval.get()) != 0:
                inventory.update_one({'Product_ID': update_ID}, {"$set":{'Product_Name':newproductval.get().strip()}})
            if len(newcpval.get()) != 0:
                inventory.update_one({'Product_ID': update_ID}, {"$set":{'Cost_Price':float(newcpval.get())}})
            if len(newspval.get()) != 0:
                inventory.update_one({'Product_ID': update_ID}, {"$set":{'Selling_Price':float(newspval.get())}})
            if len(newtaxval.get()) != 0:
                inventory.update_one({'Product_ID': update_ID}, {"$set":{'Tax':float(newtaxval.get())}})
            if len(newdiscountval.get()) != 0:
                inventory.update_one({'Product_ID': update_ID}, {"$set":{'Discount':float(newdiscountval.get())}})
            else:
                messagebox.showinfo('Update', 'Updated!')
        except ValueError:
            messagebox.showerror('Invalid Input/s', 'Cost Price, Selling Price, Tax and Discount should not be any alphabet and should be greater than zero')
    else:
        messagebox.showerror('ID Error', 'ID Not Found!')
    
    
def delete_update_entries():
    bar_entry.delete(0, 'end')
    new_product_entry.delete(0, 'end')
    new_cp_entry.delete(0, 'end')
    new_sp_entry.delete(0, 'end')
    new_tax_entry.delete(0, 'end')
    new_discount_entry.delete(0, 'end')
    find_result_label.place_forget()

def fetch_and_display_inventory():
    analytics_board.config(state=NORMAL)
    analytics_board.delete("1.0", END)

    # Fetch data from MongoDB and create DataFrame
    data = list(inventory.find())
    if not data:
        analytics_board.insert(END, "No data found in the database.")
        return

    df = pd.DataFrame(data)

    # Define columns and ensure they exist
    columns = [
        "SLNO", "Product_ID", "Product_Name", "Cost_Price", "Selling_Price",
        "Manufacture_Date", "Expire_Date", "Tax", "Discount"
    ]

    for col in columns[1:]:  # excluding SLNO
        if col not in df.columns:
            df[col] = ""

    df.insert(0, "SLNO", range(1, len(df) + 1))
    df = df[columns].fillna("")

    # Column widths
    col_widths = {
        "SLNO": 5,
        "Product_ID": 12,
        "Product_Name": 20,
        "Cost_Price": 12,
        "Selling_Price": 14,
        "Manufacture_Date": 18,
        "Expire_Date": 15,
        "Tax": 6,
        "Discount": 9
    }

    # Format lines
    separator = "|"
    format_str = separator.join(f"{{:<{col_widths[col]}}}" for col in columns)
    divider_line = "-" * (sum(col_widths.values()) + len(columns) - 1)

    # Header
    analytics_board.insert(END, format_str.format(*columns) + "\n")
    analytics_board.insert(END, divider_line + "\n")

    # Rows with dividers
    for _, row in df.iterrows():
        row_line = format_str.format(*[str(row[col]) for col in columns])
        analytics_board.insert(END, row_line + "\n")
        analytics_board.insert(END, divider_line + "\n")

    analytics_board.config(state=DISABLED)
    
def analytics_idsrc_display():
    analytics_board.config(state=NORMAL)
    analytics_board.delete("1.0", END)
    find_product_id = inventory.find_one(
        {'Product_ID':analytics_src_val.get()}
    )
    if find_product_id:
        product_dict = inventory.find_one(
            {'Product_ID':analytics_src_val.get()},
            {"Product_Name": 1,
             "Cost_Price": 1,
             "Selling_Price": 1,
             "Manufacture_Date": 1,
             "Expire_Date": 1,
             "Tax": 1,
             "Discount": 1}
        )
        arranged_product = f'''
#######---- Product Found ----#######

Product_ID:       {analytics_src_val.get()},
Product_Name:     {product_dict['Product_Name']},
Cost_Price:       {product_dict['Cost_Price']},
Selling_Price:    {product_dict['Selling_Price']},
Manufacture_Date: {product_dict['Manufacture_Date']},
Expire_Date:      {product_dict['Expire_Date']},
Tax:              {product_dict['Tax']},
Discount:         {product_dict['Discount']}
        '''
        analytics_board.insert(END, arranged_product)
    else:
        messagebox.showerror('Wrong ID', 'Product not found!')

# analytics_option = ['All', 'Cost, Selling Price', 'Product, Selling Price','Product, Cost Price', 'Product, Discount', 'Product, Tax', 'Product, Tax, Discount']

def fetch_and_display_analytics(selected_columns):
    analytics_board.config(state=NORMAL)
    analytics_board.delete("1.0", END)

    # Fetch data from MongoDB and create DataFrame
    data = list(inventory.find())
    if not data:
        analytics_board.insert(END, "No data found in the database.")
        return

    df = pd.DataFrame(data)

    # Ensure selected columns exist in DataFrame
    valid_columns = []
    for col in selected_columns:
        if col not in df.columns:
            df[col] = ""  # Add missing columns as empty if needed
        valid_columns.append(col)

    # Add SLNO at the beginning
    df.insert(0, "SLNO", range(1, len(df) + 1))
    if "SLNO" not in valid_columns:
        valid_columns.insert(0, "SLNO")

    df = df[valid_columns].fillna("")

    # Define default column widths (can be customized)
    length_list = []
    for length in selected_columns:
        length_list.append(len(length))

    default_width = max(length_list)+5
    col_widths = {
        col: (5 if col == "SLNO" else max(default_width, len(col)))
        for col in valid_columns
    }

    # Format lines
    separator = "|"
    format_str = separator.join(f"{{:<{col_widths[col]}}}" for col in valid_columns)
    divider_line = "-" * (sum(col_widths.values()) + len(valid_columns) - 1)

    # Header
    analytics_board.insert(END, format_str.format(*valid_columns) + "\n")
    analytics_board.insert(END, divider_line + "\n")

    # Rows
    for _, row in df.iterrows():
        row_line = format_str.format(*[str(row[col]) for col in valid_columns])
        analytics_board.insert(END, row_line + "\n")
        analytics_board.insert(END, divider_line + "\n")

    analytics_board.config(state=DISABLED)


def option_selected(choice):
    global choice_list
    if choice == 'All':
        fetch_and_display_inventory()
        choice_list.insert(0, 'All')

    elif choice == 'Cost, Selling Price':
        print('Choice 2')
        fetch_and_display_analytics(['Product_ID','Product_Name', 'Cost_Price', 'Selling_Price'])
        choice_list.insert(0, 'Cost, Selling Price')
        
    elif choice == 'Product, Selling Price':
        fetch_and_display_analytics(['Product_ID','Product_Name', 'Selling_Price'])
        choice_list.insert(0, 'Product, Selling Price')

    elif choice == 'Product, Cost Price':
        fetch_and_display_analytics(['Product_ID','Product_Name', 'Cost_Price'])
        choice_list.insert(0, 'Product, Cost Price')

    elif choice == 'Product, Discount':
        fetch_and_display_analytics(['Product_ID','Product_Name', 'Discount'])
        choice_list.insert(0, 'Product, Discount')
    elif choice == 'Product, Tax':
        fetch_and_display_analytics(['Product_ID','Product_Name', 'Tax'])
        choice_list.insert(0, 'Product, Tax')
    elif choice == 'Product, Tax, Discount':
        fetch_and_display_analytics(['Product_ID','Product_Name', 'Tax', 'Discount'])
        choice_list.insert(0, 'Product, Tax, Discount')
    else:
        messagebox.showerror('Invalid Option', 'Option not found!')


def export_inventory_to_excel(selected_columns):

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Save Inventory Data As"
    )

    if not file_path:
        print("Export cancelled by user.")
        return

    # Fetch data from MongoDB
    data = list(inventory.find())
    if not data:
        print("No data found in the database.")
        return

    df = pd.DataFrame(data)

    # Ensure selected columns exist
    valid_columns = []
    for col in selected_columns:
        if col not in df.columns:
            df[col] = ""
        valid_columns.append(col)

    # Add SLNO
    df.insert(0, "SLNO", range(1, len(df) + 1))
    if "SLNO" not in valid_columns:
        valid_columns.insert(0, "SLNO")

    df = df[valid_columns].fillna("")

    # Save to Excel
    try:
        df.to_excel(file_path, index=False)

        # Load workbook and format
        wb = load_workbook(file_path)
        ws = wb.active

        center_alignment = Alignment(horizontal="center", vertical="center")

        for col_idx, col_name in enumerate(valid_columns, start=1):
            col_letter = get_column_letter(col_idx)
            if col_name == "SLNO":
                ws.column_dimensions[col_letter].width = 6
            elif len(col_name) > 15:
                ws.column_dimensions[col_letter].width = len(col_name) + 5
            else:
                ws.column_dimensions[col_letter].width = 15

            for cell in ws[col_letter]:
                cell.alignment = center_alignment

        wb.save(file_path)
        messagebox.showinfo('Excel File Saved',f"Excel file saved: {file_path}")

        # Convert Excel to PDF
        pdf_path = os.path.splitext(file_path)[0] + ".pdf"
        pythoncom.CoInitialize()  # Initialize COM (required in some contexts)
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb_excel = excel.Workbooks.Open(file_path)
        wb_excel.ExportAsFixedFormat(0, pdf_path)
        wb_excel.Close(False)
        excel.Quit()
        messagebox.showinfo('PDF Saved',f"PDF file saved: {pdf_path}")

    except Exception as e:
        messagebox.showerror('Conversion Failed!',f"Failed to save or convert file: {e}")


def save_analytics_display():
    global choice_list
    try:
        if choice_list[0] == 'All':
            
            col = [
                "Product_ID", "Product_Name", "Cost_Price", "Selling_Price",
                "Manufacture_Date", "Expire_Date", "Tax", "Discount"
            ]
            export_inventory_to_excel(col)
            
        elif choice_list[0] == 'Cost, Selling Price':
            export_inventory_to_excel(['Product_ID','Product_Name', 'Cost_Price', 'Selling_Price'])
            
        elif choice_list[0] == 'Product, Selling Price':
            export_inventory_to_excel(['Product_ID','Product_Name', 'Selling_Price'])

        elif choice_list[0] == 'Product, Cost Price':
            export_inventory_to_excel(['Product_ID','Product_Name', 'Cost_Price'])

        elif choice_list[0] == 'Product, Discount':
            export_inventory_to_excel(['Product_ID','Product_Name', 'Discount'])
        elif choice_list[0] == 'Product, Tax':
            export_inventory_to_excel(['Product_ID','Product_Name', 'Tax'])
        elif choice_list[0] == 'Product, Tax, Discount':
            export_inventory_to_excel(['Product_ID','Product_Name', 'Tax', 'Discount'])
        else:
            messagebox.showerror('Invalid Option', 'Option not found!')
    except IndexError:
        messagebox.showerror('IndexError', 'No parameter Found!')

def get_cc_text():
    global username_list
    print(username_list[0])
    content_cc = cc_textbox.get("0.0", "end")  # "0.0" = start, "end-1c" = end minus last newline
    if len(content)>0:
        now = datetime.now()
        date_time_cc = now.strftime("%Y-%m-%d %H:%M:%S")
        email = client_info.find_one({'username':username_list[0]}, {'email':1})
        if email:
            Email = email['email']
            cc_message = {
                'Email':Email,
                'Time': date_time_cc,
                'Message': content_cc
            }
            cc_database.insert_one(cc_message)
            messagebox.showinfo('Customer Care', f'Message sent successfully.The reply will sent to your email {Email}')
        else:
            messagebox.showerror('Customer Care', "Can't send the message! Please login again.")
    else:
        messagebox.showerror('Customer Care', "Can't send empty message!")
        
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
    
    login_signup_database = client[r_shop_name]
    inventory = login_signup_database.stock_inventory
    
    customer_care_database = client['Customer-Care']
    cc_database = customer_care_database.cc_messages
    
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
    # inventory_display.pack(side='left')
    
    inventory_canvas=Canvas(inventory_display,height=770,width=1150,bg='blue',bd=0,highlightthickness=0, relief='ridge')
    inventory_canvas.propagate(False)
    inventory_canvas.pack()


    imagepath10=cwd+"\\uiux\\inventory.png"
    openphoto10=Image.open(imagepath10).resize((1150,770))
    bgimage10=ImageTk.PhotoImage(openphoto10)
    inventory_canvas.create_image(575,385, image=bgimage10)
    
    add_stock_button = ctk.CTkButton(inventory_display, text="Add Stocks", font=('Poppins', 25,'bold'), height=90, width = 190, cursor='hand2',
                                fg_color='white', bg_color='white', text_color='Black', hover_color='white',
                                corner_radius=10, command= stock_add)
    add_stock_button.place(x = 719, y = 50)
    
    update_product_button = ctk.CTkButton(inventory_display, text="Update Stocks", font=('Poppins', 25,'bold'), height=90, width = 188, cursor='hand2',
                                fg_color='white', bg_color='white', text_color='Black', hover_color='white',
                                corner_radius=10, command = update_stock)
    update_product_button.place(x = 817, y = 195)
    
    stock_analytics = ctk.CTkButton(inventory_display, text="Stock Analytics", font=('Poppins', 22,'bold'), height=90, width = 190, cursor='hand2',
                                fg_color='white', bg_color='white', text_color='Black', hover_color='white',
                                corner_radius=10, command=analyse_stock)
    stock_analytics.place(x = 917, y = 340)
    
    check_stock_button = ctk.CTkButton(inventory_display, text="Future Updates", font=('Poppins', 22,'bold'), height=100, width = 190, cursor='hand2',
                                fg_color='white', bg_color='white', text_color='Black', hover_color='white',
                                corner_radius=10)
    check_stock_button.place(x = 817, y = 480)
    
    most_sold_button = ctk.CTkButton(inventory_display, text="Future Updates", font=('Poppins', 22,'bold'), height=90, width = 190, cursor='hand2',
                                fg_color='white', bg_color='white', text_color='Black', hover_color='white',
                                corner_radius=10)
    most_sold_button.place(x = 719, y = 630)
    
    # =======================<<<<<<<<<<<< Add Stock Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================

    add_stock_frame=Frame(dashboard_frame,height=770,width=1150,bg='blue')
    add_stock_frame.propagate(False)
    # inventory_display.pack(side='left')
    
    add_stock_canvas=Canvas(add_stock_frame,height=770,width=1150,bg='blue',bd=0,highlightthickness=0, relief='ridge')
    add_stock_canvas.propagate(False)
    add_stock_canvas.pack()


    imagepath11=cwd+"\\uiux\\add stock.png"
    openphoto11=Image.open(imagepath11).resize((1150,770))
    bgimage11=ImageTk.PhotoImage(openphoto11)
    add_stock_canvas.create_image(575,385, image=bgimage11)

    barid = StringVar()
    
    bar_id_entry = ctk.CTkEntry(add_stock_frame, height=40,width=330, fg_color='#f2f3f4', text_color='black',
                                border_color='#4B54F8', bg_color='white', corner_radius=20, 
                                font=('Poppins', 22), textvariable= barid)
    bar_id_entry.place(x = 700, y = 125)
    
    productname = StringVar()
    
    productname_entry = ctk.CTkEntry(add_stock_frame, height=40,width=290, fg_color='#f2f3f4', text_color='black',
                                border_color='#4B54F8', bg_color='white', corner_radius=20, 
                                font=('Poppins', 22), textvariable= productname)
    productname_entry.place(x = 730, y = 195)
    
    productqty = StringVar()
    
    productQuantity_entry = ctk.CTkEntry(add_stock_frame, height=40,width=290, fg_color='#f2f3f4', text_color='black',
                                border_color='#4B54F8', bg_color='white', corner_radius=20, 
                                font=('Poppins', 22), textvariable= productqty)
    productQuantity_entry.place(x = 730, y = 260)
    
    cp = StringVar()
    
    cp_entry = ctk.CTkEntry(add_stock_frame, height=40,width=290, fg_color='#f2f3f4', text_color='black',
                                border_color='#4B54F8', bg_color='white', corner_radius=20, 
                                font=('Poppins', 22),  textvariable= cp)
    cp_entry.place(x = 730, y = 325)
    
    sp = StringVar()
        
    sp_entry = ctk.CTkEntry(add_stock_frame, height=40,width=290, fg_color='#f2f3f4', text_color='black',
                                border_color='#4B54F8', bg_color='white', corner_radius=20, 
                                font=('Poppins', 22), textvariable = sp)
    sp_entry.place(x = 730, y = 390)
    
    tax = StringVar()
    
    tax_entry = ctk.CTkEntry(add_stock_frame, height=40,width=290, fg_color='#f2f3f4', text_color='black',
                                border_color='#4B54F8', bg_color='white', corner_radius=20, 
                                font=('Poppins', 22), textvariable= tax)
    tax_entry.place(x = 730, y = 455)
    
    mfdate = StringVar()

    mf_date_entry = ctk.CTkEntry(add_stock_frame, height=40,width=200, fg_color='#f2f3f4', text_color='black',
                                border_color='#4B54F8', bg_color='white', corner_radius=20, font=('Poppins', 22),
                                textvariable = mfdate)
    mf_date_entry.place(x = 780, y = 530)
    
    calendar_pil_image = Image.open(cwd+"\\uiux\\Calendar.png")
    calendar_icon = ctk.CTkImage(light_image=calendar_pil_image, dark_image=calendar_pil_image, size=(32, 32))
    
    calendar_button = ctk.CTkButton(add_stock_frame, image=calendar_icon, text="", width=40, height=40, fg_color= "white",
                                    bg_color="white", hover_color="white", cursor = 'hand2', command=open_calendar)
    calendar_button.place( x = 980, y = 530)
    
    expdate = StringVar()
    
    exp_date_entry = ctk.CTkEntry(add_stock_frame, height=40,width=200, fg_color='#f2f3f4', text_color='black',
                                border_color='#4B54F8', bg_color='white', corner_radius=20, font=('Poppins', 22),
                                textvariable= expdate)
    exp_date_entry.place(x = 780, y = 600)

    calendar_pil_image1 = Image.open(cwd+"\\uiux\\Calendar.png")
    calendar_icon1 = ctk.CTkImage(light_image=calendar_pil_image1, dark_image=calendar_pil_image1, size=(32, 32))
    
    calendar_button = ctk.CTkButton(add_stock_frame, image=calendar_icon1, text="", width=40, height=40, fg_color= "white",
                                    bg_color="white", hover_color="white", cursor = 'hand2', command=open_calendar1)
    calendar_button.place( x = 980, y = 600)
    
    
    add_stocks_button = ctk.CTkButton(add_stock_frame, text="Add", font=('arial', 26, 'bold'), height=45, width = 40, cursor='hand2',
                                fg_color='#2ecc71', bg_color='white', text_color='white', hover_color='black', 
                                corner_radius=10, command= add_stock)
    add_stocks_button.place(x = 595, y = 660)
    back_button = ctk.CTkButton(add_stock_frame, text="Back", font=('arial', 26, 'bold'), height=45, width = 40, cursor='hand2',
                                fg_color='#8e44ad', bg_color='white', text_color='white', 
                                hover_color='black', corner_radius=10, command=back_stock_entry)
    back_button.place(x = 750, y = 660)
    clear_button = ctk.CTkButton(add_stock_frame, text="Clear", font=('arial', 26, 'bold'), height=45, width = 40, cursor='hand2',
                                fg_color='#e74c3c', bg_color='white', text_color='white', 
                                hover_color='black', corner_radius=10, command= clear_inventory_entries
                                )
    clear_button.place(x = 900, y = 660)
    
    # =======================<<<<<<<<<<<< Add Stock Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================

    update_stock_frame=Frame(dashboard_frame,height=770,width=1150,bg='blue')
    update_stock_frame.propagate(False)
    # inventory_display.pack(side='left')
    
    update_stock_canvas=Canvas(update_stock_frame,height=770,width=1150,bg='blue',bd=0,highlightthickness=0, relief='ridge')
    update_stock_canvas.propagate(False)
    update_stock_canvas.pack()


    imagepath12=cwd+"\\uiux\\update_stock2.png"
    openphoto12=Image.open(imagepath12).resize((1150,770))
    bgimage12=ImageTk.PhotoImage(openphoto12)
    update_stock_canvas.create_image(575,385, image=bgimage12)
    
    item_id_in_update = StringVar()
    
    bar_entry = ctk.CTkEntry(update_stock_frame, height=40,width=303, fg_color='white', text_color='black',
                             bg_color='white', corner_radius=20, font=('Poppins', 22), border_color='white',
                             textvariable= item_id_in_update)
    bar_entry.place(x = 585, y = 118)
    
    find_result_label = Label(update_stock_frame, text='', font=('poppins', 18, 'bold'), bg ='#4B54F8',
                              anchor='w', fg='white')
    
    
    id_src_button = ctk.CTkButton(update_stock_frame, text="Search", font=('Popins', 26, 'bold'), height=45, width = 40, cursor='hand2',
                                fg_color='#4B54F8', bg_color='white', text_color='white', 
                                hover_color='black', corner_radius=10, command= find_item_in_update)
    id_src_button.place(x = 940, y = 118)
    
    
    found_product_label = ctk.CTkLabel(update_stock_frame, text="", font=("poppins", 18), 
                                       fg_color = 'white', text_color='white')
    found_product_label.place( x = 585, y = 190)
    
    newproductval = StringVar()
    
    new_product_entry = ctk.CTkEntry(update_stock_frame, height=40,width=290, fg_color='#f2f3f4', text_color='black',
                                border_color='#4B54F8', bg_color='white', corner_radius=20, 
                                font=('Poppins', 22), textvariable=newproductval)
    new_product_entry.place(x = 800, y = 230)
    
    newcpval = StringVar()
    
    new_cp_entry = ctk.CTkEntry(update_stock_frame, height=40,width=290, fg_color='#f2f3f4', text_color='black',
                                border_color='#4B54F8', bg_color='white', corner_radius=20, 
                                font=('Poppins', 22), textvariable= newcpval)
    new_cp_entry.place(x = 800, y = 285)
    
    newspval = StringVar()
    
    new_sp_entry = ctk.CTkEntry(update_stock_frame, height=40,width=290, fg_color='#f2f3f4', text_color='black',
                                border_color='#4B54F8', bg_color='white', corner_radius=20, 
                                font=('Poppins', 22), textvariable=newspval)
    new_sp_entry.place(x = 800, y = 345)
    
    newtaxval = StringVar()
    
    new_tax_entry = ctk.CTkEntry(update_stock_frame, height=40,width=290, fg_color='#f2f3f4', text_color='black',
                                border_color='#4B54F8', bg_color='white', corner_radius=20, 
                                font=('Poppins', 22), textvariable=newtaxval)
    new_tax_entry.place(x = 800, y = 405)
    
    newdiscountval = StringVar()
    
    new_discount_entry = ctk.CTkEntry(update_stock_frame, height=40,width=290, fg_color='#f2f3f4', text_color='black',
                                border_color='#4B54F8', bg_color='white', corner_radius=20, 
                                font=('Poppins', 22), textvariable = newdiscountval)
    new_discount_entry.place(x = 800, y = 465)
    
    
    update_button = ctk.CTkButton(update_stock_frame, text="Update", font=('Popins', 26, 'bold'), height=45, width = 40, cursor='hand2',
                                fg_color='#4B54F8', bg_color='white', text_color='white', 
                                hover_color='black', corner_radius=10, command=update_product)
    update_button.place(x = 615, y = 530)
    
    
    update_back_button = ctk.CTkButton(update_stock_frame, text="Back", font=('Popins', 26, 'bold'), height=45, width = 40, cursor='hand2',
                                fg_color='#4B54F8', bg_color='white', text_color='white', 
                                hover_color='black', corner_radius=10, command=back_update_entry)
    update_back_button.place(x = 790, y = 530)
    
    update_clear_button = ctk.CTkButton(update_stock_frame, text="Clear", font=('Popins', 26, 'bold'), height=45, width = 40, cursor='hand2',
                                fg_color='#4B54F8', bg_color='white', text_color='white', 
                                hover_color='black', corner_radius=10, command = delete_update_entries)
    update_clear_button.place(x = 935, y = 530)
    
    # =======================<<<<<<<<<<<< Add stock analytics INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================

    stock_analytics_frame=Frame(dashboard_frame,height=770,width=1150,bg='blue')
    stock_analytics_frame.propagate(False)
    # inventory_display.pack(side='left')
    
    stock_analytics_canvas=Canvas(stock_analytics_frame,height=770,width=1150,bg='blue',bd=0,highlightthickness=0, relief='ridge')
    stock_analytics_canvas.propagate(False)
    stock_analytics_canvas.pack()


    imagepath13=cwd+"\\uiux\\analytics.png"
    openphoto13=Image.open(imagepath13).resize((1150,770))
    bgimage13=ImageTk.PhotoImage(openphoto13)
    stock_analytics_canvas.create_image(575,385, image=bgimage13)
    
    
    analytics_board = Text(stock_analytics_frame, wrap="none", height=25, width=136, relief='ridge', bd=3,
                           state= DISABLED, fg='black')
    analytics_board.place(x = 20, y = 42)
    
    v_scroll = ctk.CTkScrollbar(stock_analytics_frame, orientation="vertical", command=analytics_board.yview, bg_color='white', 
                                height=405)
    v_scroll.place(x = 1120, y = 42)
    
    h_scroll = ctk.CTkScrollbar(stock_analytics_frame, orientation="horizontal", command=analytics_board.xview,
                                width=1090, bg_color='white')
    h_scroll.place(x = 24, y = 455)
    
    analytics_board.config(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    
    analytics_src_val = StringVar()
    
    analytics_src_entry = ctk.CTkEntry(stock_analytics_frame, font=('Poppins', 18), fg_color = 'white',
                                       bg_color='white', border_color='#4B54F8', corner_radius=20,
                                       height=30, width=250, textvariable=analytics_src_val)
    analytics_src_entry.place(x = 350, y = 520)
    
    analytics_src_button = ctk.CTkButton(stock_analytics_frame, text="Search", font=('Popins', 18, 'bold'), height=15, width = 175, cursor='hand2',
                                fg_color='#17a589', bg_color='white', text_color='white', 
                                hover_color='black', corner_radius=30, anchor='center', command = analytics_idsrc_display)
    analytics_src_button.place( x = 630, y = 522)
    
    analytics_option = ['All', 'Cost, Selling Price', 'Product, Selling Price','Product, Cost Price', 'Product, Discount', 'Product, Tax', 'Product, Tax, Discount']
    
    analytics_option_menu = ctk.CTkOptionMenu(stock_analytics_frame, values=analytics_option, bg_color='white', fg_color='#4B54F8',
                                              font=('Poppins', 15, 'bold'), text_color='white', width= 250,
                                              button_color='black', button_hover_color='grey', command=option_selected)
    analytics_option_menu.set(analytics_option[0])  # Set default option
    analytics_option_menu.place(x = 450, y = 570)

    analytics_back_button = ctk.CTkButton(stock_analytics_frame, text="Back", font=('Popins', 18, 'bold'), height=15, width = 120, cursor='hand2',
                                fg_color='#e74c3c', bg_color='white', text_color='white', 
                                hover_color='black', corner_radius=30, anchor='center', command = analytics_back)
    analytics_back_button.place( x = 315, y = 640)
    
    analytics_reset_button = ctk.CTkButton(stock_analytics_frame, text="Reset", font=('Popins', 18, 'bold'), height=15, width = 120, cursor='hand2',
                                fg_color='#2e86c1', bg_color='white', text_color='white', 
                                hover_color='black', corner_radius=30, anchor='center', command = fetch_and_display_inventory)
    analytics_reset_button.place( x = 450, y = 640)
    
    analytics_print_button = ctk.CTkButton(stock_analytics_frame, text="Print", font=('Popins', 18, 'bold'), height=15, width = 120, cursor='hand2',
                                fg_color='#7d3c98', bg_color='white', text_color='white', 
                                hover_color='black', corner_radius=30, anchor='center')
    analytics_print_button.place( x = 585, y = 640)
    
    analytics_save_button = ctk.CTkButton(stock_analytics_frame, text="Save", font=('Popins', 18, 'bold'), height=15, width = 120, cursor='hand2',
                                fg_color='#616a6b', bg_color='white', text_color='white', 
                                hover_color='black', corner_radius=30, anchor='center', command = save_analytics_display)
    analytics_save_button.place( x = 720, y = 640)
    # =======================<<<<<<<<<<<< alert Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================

    alert_display=Frame(dashboard_frame,height=770,width=1150,bg='green')
    alert_display.propagate(False)
    # alert_display.pack(side='left')
    
    # =======================<<<<<<<<<<<< billing Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================
    
    billing_display=Frame(dashboard_frame,height=770,width=1150,bg='yellow')
    billing_display.propagate(False)
    # billing_display.pack(side='left')
    
    # =======================<<<<<<<<<<<< supply Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================
    
    supply_display=Frame(dashboard_frame,height=770,width=1150,bg='pink')
    supply_display.propagate(False)
    # supply_display.pack(side='left')
    
    # =======================<<<<<<<<<<<< history Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================
    
    history_display=Frame(dashboard_frame,height=770,width=1150,bg='violet')
    history_display.propagate(False)
    # history_display.pack(side='left')
    
    # =======================<<<<<<<<<<<< setting Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================
    
    setting_display=Frame(dashboard_frame,height=770,width=1150,bg='brown')
    setting_display.propagate(False)
    # setting_display.pack(side='left')
    
    # =======================<<<<<<<<<<<< cc Display INTERFACE FROM HERE >>>>>>>>>>>>>>>=============================
    
    cc_display=Frame(dashboard_frame,height=770,width=1150,bg='grey')
    cc_display.propagate(False)
    # cc_display.pack(side='left')
    cc_canvas=Canvas(cc_display,height=770,width=1150,bg='blue',bd=0,highlightthickness=0, relief='ridge')
    cc_canvas.propagate(False)
    cc_canvas.pack()


    imagepath14=cwd+"\\uiux\\cc3.png"
    openphoto14=Image.open(imagepath14).resize((1150,770))
    bgimage14=ImageTk.PhotoImage(openphoto14)
    cc_canvas.create_image(575,385, image=bgimage14)
    
    
    cc_textbox = ctk.CTkTextbox(cc_display, width=400, height=200, bg_color = 'white', fg_color='#d6eaf8', 
                                scrollbar_button_color='#4B54F8', border_color='red', font=('poppins', 12, 'bold'),border_width=1)
    cc_textbox.place(x = 640, y = 200)

    cc_send_button = ctk.CTkButton(cc_display, text="Send Message", font=('poppins', 18, 'bold'),command=get_cc_text, 
                                   fg_color='#4B54F8', bg_color='white', text_color='white', corner_radius=20,
                                   hover_color='black')
    cc_send_button.place(x = 775, y = 450)

    win.mainloop()
    
else:
    messagebox.showerror('Connection Error', 'Please Check your internet connection!')


