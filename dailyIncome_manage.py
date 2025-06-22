# import sqlite3

# # Connect to (or create) a database file
# conn = sqlite3.connect('Data\\dailyEarnings.db')  # Change the file name if needed
# cursor = conn.cursor()

# # Create the table if it doesn't exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS IncomeTable (
#         Dates TEXT,
#         Income REAL
#     )
# ''')

# # Commit the changes and close the connection
# conn.commit()
# conn.close()




# import sqlite3

# # Connect to the database
# conn = sqlite3.connect('Data\\dailyEarnings.db')
# cursor = conn.cursor()

# # Fetch Dates and Income from the table
# cursor.execute("SELECT Dates, Income FROM IncomeTable")
# rows = cursor.fetchall()

# # Separate the results into two lists
# dates = [row[0] for row in rows]
# income = [row[1] for row in rows]

# # Close the connection
# conn.close()

# # (Optional) Print to verify
# print("Dates:", dates)
# print("Income:", income)

import sqlite3

def upsert_income(date, income):
    # Connect to the database
    conn = sqlite3.connect('Data\\dailyEarnings.db')
    cursor = conn.cursor()

    # Check if the date exists
    cursor.execute("SELECT 1 FROM IncomeTable WHERE Dates = ?", (date,))
    result = cursor.fetchone()

    if result:
        # Update existing record
        cursor.execute("UPDATE IncomeTable SET Income = ? WHERE Dates = ?", (income, date))
        print(f"Updated income for date {date}")
    else:
        # Insert new record
        cursor.execute("INSERT INTO IncomeTable (Dates, Income) VALUES (?, ?)", (date, income))
        print(f"Inserted new income for date {date}")

    # Commit and close
    conn.commit()
    conn.close()

datess = [
    "2025-06-14", "2025-06-15", "2025-06-16", "2025-06-17",
    "2025-06-18", "2025-06-19", "2025-06-20", "2025-06-21"
]


earningss = [
    1200, 1500, 800, 1800, 2100, 
    1900, 1300, 1000
]
for date, income in zip(datess, earningss):
    upsert_income(date, income)


# # Connect to the database
# conn = sqlite3.connect('Data\\dailyEarnings.db')
# cursor = conn.cursor()

# # Insert the data
# for date, income in zip(datess, earningss):
#     cursor.execute("INSERT INTO IncomeTable (Dates, Income) VALUES (?, ?)", (date, income))

# # Commit and close
# conn.commit()
# conn.close()

# print("Data inserted successfully.")
