from tkinter import *
import customtkinter as ctk
import random
import string
from tkinter import messagebox
import os 
from pathlib import Path
from pymongo import MongoClient
import socket
from dotenv import load_dotenv
shopid = []
shopnameID = []

def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        # Attempt to connect to a well-known DNS server (Google)
        socket.setdefaulttimeout(timeout)
        with socket.create_connection((host, port)):
            return True
    except OSError:
        return False

def handle_listed_checkboxes():
    if listed_yes_var.get():
        listed_no_var.set(0)
        shopid_label.place(x = 20, y = 120)
        shopid_entry.place(x = 150, y = 120)
        multi_label.place_forget()
        multi_yes_cb.place_forget()
        multi_no_cb.place_forget()
        continue_button.place(x = 300, y = 300)
        clear_generated_id()
        
    elif listed_no_var.get():
        listed_yes_var.set(0)
        shopid_label.place_forget()
        shopid_entry.place_forget()
        multi_label.place(x = 20, y = 160)
        multi_yes_cb.place(x = 20, y = 190)
        multi_no_cb.place(x = 100, y = 190)
        continue_button.place_forget()

    else:
        shopid_label.place_forget()
        shopid_entry.place_forget()
        multi_label.place_forget()
        multi_yes_cb.place_forget()
        multi_no_cb.place_forget()
        clear_generated_id()
        continue_button.place_forget()
        
        
def handle_multi_cashier_checkboxes():
    if multi_yes_var.get():
        multi_no_var.set(0)
        generate_shop_id()
        continue_button.place(x = 300, y = 300)
    elif multi_no_var.get():
        multi_yes_var.set(0)
        generate_shop_id()
        continue_button.place(x = 300, y = 300)
        
    else:
        clear_generated_id()
        continue_button.place_forget()

def generate_shop_id():
    global shopid
    
    shop_id = "BZ" + ''.join(random.choices(string.digits + string.ascii_uppercase, k=6))
    find_if_dup = collection.find_one({"ShopID":shop_id})
    if not find_if_dup:
        shopid.insert(0, shop_id)
        generated_id_label.configure(text=f"Generated Shop ID: {shop_id}\nPlease write this ID somewhere.")
        generated_id_label.place(x = 20, y = 220)
    else:
        generate_shop_id()
    
def clear_generated_id():
    generated_id_label.configure(text="")
    generated_id_label.place_forget()
    
def open_tnc():
    
    global shopnameID
    if shopname_entry.get():
        if listed_no_var.get():
            shop_details_frame.pack_forget()
            tnc_frame.pack(fill='both', expand=True)
        elif listed_yes_var.get():
            if shopid_entry.get():
                shop_name = shopname_entry.get().title().replace(' ', '') + shopid_entry.get().strip()
                find_shopnameID = collection.find_one({"Shopname ID":shop_name})
                if find_shopnameID:
                    find_if_multi = collection.find_one({"Shopname ID":shop_name}, {"Multi Store":1})
                    if find_if_multi["Multi Store"] == 1:
                        shopnameID.insert(0, shop_name)
                        shop_details_frame.pack_forget()
                        tnc_frame.pack(fill='both', expand=True)
                        messagebox.showinfo('Shop Listed', 'Your shop is listed on Bazaro..')
                    else:
                        messagebox.showinfo("No Multi store", "The shop is registered as 'NO MULTI STORE' on Bazaro. Thus No more than one login.")
                else:
                    messagebox.showwarning('Unlisted', 'Your shop is not listed on Bazaro..')
            else:
                messagebox.showwarning('Shop ID', 'Please provide the shop ID before procceeding.')
    else:
        messagebox.showwarning('Shop Name', 'Please provide the shop name before procceeding.')

def insert_shopname_to_txt():
    global shopid
    print("Not listed on Bazaro")
    shop_name = shopname_entry.get().title().replace(' ', '') + shopid[0]
    print(shop_name)
    # Define the filename
    current_dir_setup = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
    filename = current_dir_setup/"shopname.txt"

    # Open the file in write mode ('w') – this will overwrite the file if it already exists
    with open(filename, "w") as file:
        file.write(shop_name)
    file.close()

    collection.insert_one({
        "ShopID": shopid[0],
        "Shop Name":shopname_entry.get().title(),
        "Shopname ID":shop_name,
        "Multi Store": multi_yes_var.get(),
        "Total Users": 1 
    })
    
def on_submit():
    global shopnameID
    if agree_var.get():
        if listed_no_var.get():
            messagebox.showinfo("Success", "Thank you for agreeing. You may proceed.")
            insert_shopname_to_txt()
        elif listed_yes_var.get():
            print("Shop Already listed!")
            current_dir_setup = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
            filename = current_dir_setup/"shopname2.txt"
            with open(filename, "w") as file:
                file.write(shopnameID[0])
            file.close()
            total_users_get = collection.find_one({"Shopname ID":shopnameID[0]}, {"Total Users":1})
            total_users_count = total_users_get["Total Users"] + 1
            collection.update_one({"Shopname ID":shopnameID[0]}, {"$set":{"Total Users":total_users_count}})
            messagebox.showinfo("Success", "Thank you for agreeing. You may proceed.")
        # Proceed to next step in app setup
    else:
        messagebox.showwarning("Agreement Required", "Please agree to the Terms and Conditions to continue.")
    
    submit_btn.configure(state = DISABLED)
    setup_win.destroy()
        
# Configure CTk appearance
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars_db = current_dir/ ".env"
load_dotenv(envars_db)

# Initialize the client
client = MongoClient(os.getenv('URL_Mongo'))

db = client['Login-Signup']

# Access a collection
collection = db['ShopnameId']

if check_internet():
    setup_win = Tk()

    setup_win.geometry("700x500")
    setup_win.title("Bazaro - Setup")

    shop_details_frame = Frame(setup_win, bg="white")
    shop_details_frame.propagate(False)
    shop_details_frame.pack(fill='both', expand=True )

    shopname_label = Label(shop_details_frame, text="Enter Your Shop Name:", font=('poppins', 12, 'bold'), fg="black",bg="white")
    shopname_label.pack(side='left', anchor='nw', padx=(20, 5) ,pady=(20, 5))

    shopname_entry = ctk.CTkEntry(shop_details_frame, font=('poppins', 12), fg_color='white', 
                                bg_color='white', border_color='black', height=25, width=300)
    shopname_entry.pack(side = 'left', anchor='nw',pady=20)

    listed_label = ctk.CTkLabel(shop_details_frame, text="Is your shop already listed on Bazaro?", 
                                text_color="black", font=("poppins", 13, 'bold'))
    listed_label.place(x = 20, y = 60)

    listed_yes_var = IntVar()
    listed_no_var = IntVar()

    listed_yes_cb = ctk.CTkCheckBox(shop_details_frame, text="Yes", variable=listed_yes_var, command=handle_listed_checkboxes)
    listed_no_cb = ctk.CTkCheckBox(shop_details_frame, text="No", variable=listed_no_var, command=handle_listed_checkboxes)
    listed_yes_cb.place(x = 20, y = 90)
    listed_no_cb.place(x = 100, y = 90)

    shopid_label = ctk.CTkLabel(shop_details_frame, text="Enter your Shop ID:", text_color="black", font=("poppins", 13, 'bold'))
    shopid_entry = ctk.CTkEntry(shop_details_frame, font=('poppins', 11), width=200, border_color="black", text_color="black")


    multi_yes_var = IntVar()
    multi_no_var = IntVar()

    multi_label = ctk.CTkLabel(shop_details_frame, text="Do you want Bazaro for multi-cashier use?", text_color="black", font=("poppins", 13, 'bold'))
    multi_yes_cb = ctk.CTkCheckBox(shop_details_frame, text="Yes", variable=multi_yes_var, command=handle_multi_cashier_checkboxes)
    multi_no_cb = ctk.CTkCheckBox(shop_details_frame, text="No", variable=multi_no_var, command=handle_multi_cashier_checkboxes)

    generated_id_label = ctk.CTkLabel(shop_details_frame, text="", text_color="green", font=("poppins", 11))



    continue_button = ctk.CTkButton(shop_details_frame, text="Continue", font=('poppins', 16, 'bold'),
                                    fg_color="blue", bg_color="white", text_color='white', height=30, width=100, corner_radius=20,
                                    command= open_tnc)

    tnc_frame = Frame(setup_win)
    tnc_frame.propagate(False)

    tnc_lable = Label(tnc_frame, text="Terms & Conditions", font=("poppins", 18, 'bold'), fg="black")
    tnc_lable.pack()
    terms_text = """
    By accessing, installing, or in any way using the Bazaro application — which is a shop and inventory management system developed by an individual in their capacity as a college student for project purposes but now gradually being converted into a product-level solution — the user hereby acknowledges and agrees to all the terms and conditions as laid out, regardless of whether the user has actually read them in part or in full. The Bazaro application collects and stores various pieces of information and data including, but not limited to, user email addresses, contact phone numbers, details pertaining to shop inventory and stock movement, transactional data including billing histories, and other metadata that may be necessary for the operation and improvement of the application. This data is stored in online cloud storage, specifically within the infrastructure provided by MongoDB Atlas, a third-party database-as-a-service provider. It is to be clearly understood that while reasonable precautions have been undertaken to ensure that data is transmitted and stored in a secure manner, the developer of the Bazaro application assumes no responsibility or liability in the event of any unintended access, loss, breach, corruption, or exposure of said data that may occur due to failures, misconfigurations, vulnerabilities, outages, or other technical anomalies arising from MongoDB Atlas or any other linked service or dependency. Users agree that by continuing to use the application, they consent to the storage and handling of their data in such a manner, and acknowledge that the developer, being an independent student entity and not a registered company or organization, provides the software as-is, with no guarantees, no warranties, and no claims of fitness for any particular purpose. Furthermore, the user waives any right to litigation, dispute, or demand of compensation for issues arising from the use of the app, whether due to data loss, system failure, or any other technical or non-technical matter. Continued usage of the app implies total, unconditional acceptance of all of the above.
    """

    # Scrollable textbox for the boring terms
    textbox = ctk.CTkTextbox(tnc_frame, width=600, height=300, wrap="word", corner_radius=20, fg_color='white',
                            bg_color='white', border_color='black', font=('poppins', 12), border_width=2)
    textbox.insert("0.0", terms_text)
    textbox.configure(state="disabled")  # Make it read-only
    textbox.pack(padx=20, pady=(20, 10))

    # Checkbox for user agreement
    agree_var = ctk.BooleanVar()
    agree_checkbox = ctk.CTkCheckBox(tnc_frame, text="I agree to the Terms and Conditions", variable=agree_var)
    agree_checkbox.pack(pady=10)

    # Continue button
    submit_btn = ctk.CTkButton(tnc_frame, text="Continue", command=on_submit)
    submit_btn.pack(pady=10)


    setup_win.mainloop()
else:
    messagebox.showwarning('Connection Error', 'Please Check your internet connection.')