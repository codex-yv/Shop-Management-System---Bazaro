# import time
# from datetime import datetime

# try:
#     while True:
#         # Get current date and time
#         now = datetime.now()

#         # Format day, date, and time
#         day = now.strftime("%A")  # Full weekday name
#         date_time = now.strftime("%Y-%m-%d %H:%M:%S")

#         # Clear the terminal screen (optional)
#         print("\033c", end="")

#         # Print current day, date, and time
#         print("Current Day       :", day)
#         print("Current Date/Time :", date_time)

#         # Wait for 1 second before updating
#         time.sleep(1)

# except KeyboardInterrupt:
#     print("\nProgram stopped by user.")


from datetime import datetime

# Get today's day as a number (01 to 31)
day_of_month = datetime.today().day

print(day_of_month/31)
