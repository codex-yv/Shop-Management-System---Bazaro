# mqim woqd jrkf sdkv
import os 
import random
import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv

def generate_otp():
    return random.randint(100000, 999999)

otp = generate_otp()
print(f"Your 6-digit OTP is: {otp}")

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir/ ".env"

load_dotenv(envars)

sender_email = os.getenv('EMAIL')
sender_key = os.getenv('KEY')

server.login(sender_email, sender_key)

to_mail = 'yourajverma960@gmail.com'

msg = EmailMessage()

msg['Subject'] = 'OTP verification'
msg['From'] = 'ytgamings802212@gmail.com'
msg['to'] = to_mail

msg.set_content("Your OTP is " + str(otp))

server.send_message(msg)

print("email sent")