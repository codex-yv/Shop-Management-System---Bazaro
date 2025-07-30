import requests
import time
url = "https://sms-backend-90tc.onrender.com/login"
payload = {
    "username":"Youraj Verma",
    "password":"856856"
}
response = requests.get(url, params=payload)
print(response.json())

url = "https://sms-backend-90tc.onrender.com"
response = requests.get(url)
value = response.json()
print(value)
# def find():
#     try:
        
        
#     except requests.exceptions.RequestException as e:
#         print(f"Error in find(): ")

# while True:
#     try:
        
#     except requests.exceptions.RequestException as e:
#         print(f"Error in find(): ")
#     time.sleep(1)
#     find()
#     time.sleep(1)