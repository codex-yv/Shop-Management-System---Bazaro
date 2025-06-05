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


from pymongo import MongoClient

# Replace with your MongoDB Atlas connection string
uri = "mongodb+srv://bazaodemo:mongodb856@cluster0.fgw70na.mongodb.net/"

# Connect to MongoDB
client = MongoClient(uri)

# Select the database and collection
db = client["sdarsh-sirana-store"]
collection = db["Earnings"]

# Data to be inserted
# data = {
#     "Earning_ID": 101,
#     "Daily_Income": 1000,
#     "Weekly_Income": 10000,
#     "Monthly_Income": 100000
# }

# # Insert the data
# insert_result = collection.insert_one(data)
# print(f"Inserted document with ID: {insert_result.inserted_id}")

# Fetch all documents
# all_documents = collection.find()

# Print each document's 'date' field if it exists
# for doc in all_documents:
#     print(doc.get("date", "No 'date' field"))

daily_earning = collection.find_one({"Earning_ID":101}, {"Daily_Income":1})
print(daily_earning["Daily_Income"])

# from datetime import datetime

# # Get current date
# now = datetime.now()

# # Extract year, month, and day
# YEAR = now.year
# MONTH = now.month
# DATE = now.day

# # Print the values
# print("Year:", YEAR)
# print("Month:", MONTH)
# print("Date:", DATE)

# from datetime import datetime, timedelta

# def get_week_dates(date_str):
#     # Convert the string to a datetime object
#     given_date = datetime.strptime(date_str, "%d/%m/%Y")

#     # Find the Monday of the current week
#     start_of_week = given_date - timedelta(days=given_date.weekday())

#     # Generate all dates from Monday to Sunday
#     week_dates = [(start_of_week + timedelta(days=i)).strftime("%d/%m/%Y") for i in range(7)]
#     return week_dates

# # Example usage
# date_input = "09/06/2025"
# week_list = get_week_dates(date_input)
# print("Week Dates (Monday to Sunday):")
# print(week_list)
