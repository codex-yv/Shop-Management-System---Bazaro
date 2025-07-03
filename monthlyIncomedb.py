import sqlite3
import os 
# Connect to (or create) a SQLite database
cwd = os.getcwd()
path = os.path.join(cwd, "Data", "monthly_income_data.db")
conn = sqlite3.connect(path)
cursor = conn.cursor()

# Create table if it does not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT NOT NULL,
        year INTEGER NOT NULL,
        income REAL NOT NULL
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Table 'income' created successfully (if it didn't exist already).")

# def insert_yearly_income(year, monthly_incomes):
#     # Check that 12 months of income are provided
#     if len(monthly_incomes) != 12:
#         raise ValueError("You must provide 12 monthly income values.")
    
#     # List of months in order
#     months = [
#         "January", "February", "March", "April", "May", "June",
#         "July", "August", "September", "October", "November", "December"
#     ]
    
#     # Connect to the database
#     conn = sqlite3.connect(path)
#     cursor = conn.cursor()
    
#     # Insert each month's income
#     for i in range(12):
#         cursor.execute('''
#             INSERT INTO income (month, year, income)
#             VALUES (?, ?, ?)
#         ''', (months[i], year, monthly_incomes[i]))
    
#     # Commit changes and close connection
#     conn.commit()
#     conn.close()
#     print(f"Inserted income data for the year {year}.")

# # Example usage
# monthly_income_values = [
#     4000, 4100, 4200, 4300, 4400, 4500,
#     4600, 4700, 4800, 4900, 5000, 5100
# ]

# insert_yearly_income(2025, monthly_income_values)

# import sqlite3

# def insert_or_update_income(month, year, earning):
#     conn = sqlite3.connect(path)
#     cursor = conn.cursor()
    
#     # Check if a record for this month and year already exists
#     cursor.execute('''
#         SELECT id FROM income WHERE month = ? AND year = ?
#     ''', (month, year))
    
#     result = cursor.fetchone()
    
#     if result:
#         # Record exists, update it
#         cursor.execute('''
#             UPDATE income SET income = ? WHERE month = ? AND year = ?
#         ''', (earning, month, year))
#         print(f"Updated income for {month} {year} to {earning}.")
#     else:
#         # Record doesn't exist, insert new
#         cursor.execute('''
#             INSERT INTO income (month, year, income) VALUES (?, ?, ?)
#         ''', (month, year, earning))
#         print(f"Inserted income for {month} {year}: {earning}.")
    
#     conn.commit()
#     conn.close()

# # Example usage:
# insert_or_update_income('July', 2025, 5500.00)
# insert_or_update_income('August', 2026, 5800.00)



# import sqlite3

# def get_income_by_year(year):
#     # Connect to the database
#     conn = sqlite3.connect(path)
#     cursor = conn.cursor()

#     # Retrieve data for the specified year, ordered by month if needed
#     cursor.execute('''
#         SELECT month, income
#         FROM income
#         WHERE year = ?
#     ''', (year,))

#     results = cursor.fetchall()

#     # Separate into two lists
#     month_list = [row[0] for row in results]
#     income_list = [row[1] for row in results]

#     # Close the connection
#     conn.close()

#     return month_list, income_list

# # Example usage
# month_list, income_list = get_income_by_year(2025)

# print("Months:", month_list)
# print("Income:", income_list)
