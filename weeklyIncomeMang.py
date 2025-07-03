import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('Data\\weeklyEarnings.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS IncomeTable (
    Week TEXT,
    Month TEXT,
    Income REAL,
    PRIMARY KEY (Week, Month)
)
''')

# Function to insert or update income
def upsert_income(week, month, income):
    cursor.execute('''
    INSERT INTO IncomeTable (Week, Month, Income)
    VALUES (?, ?, ?)
    ON CONFLICT(Week, Month) DO UPDATE SET
        Income = excluded.Income
    ''', (week, month, income))
    conn.commit()

# Example usage
# upsert_income("Week1", "June", 1500.00)   # Insert
# May
# July
upsert_income("Week1", "Apr", 640)
upsert_income("Week2", "Apr", 610)
upsert_income("Week3", "Apr", 665)
upsert_income("Week4", "Apr", 630)

upsert_income("Week1", "May", 625)
upsert_income("Week2", "May", 590)
upsert_income("Week3", "May", 645)
upsert_income("Week4", "May", 610)

# June
upsert_income("Week1", "Jun", 630)
upsert_income("Week2", "Jun", 600)
upsert_income("Week3", "Jun", 655)
upsert_income("Week4", "Jun", 620)
upsert_income("Week5", "Jun", 820)


# # Close connection
conn.close()


import sqlite3
from datetime import datetime
from calendar import month_abbr

# Get current month as short name (e.g., "Jun")
now = datetime.now()
current_month_index = now.month
all_months = [month_abbr[i] for i in range(1, 13)]  # ['Jan', 'Feb', ..., 'Dec']

# Get the last 3 months including current
recent_months = [all_months[(current_month_index - i - 1) % 12] for i in range(3)]

# Connect to the database
conn = sqlite3.connect('Data\\weeklyEarnings.db')
cursor = conn.cursor()

# Prepare and execute the query
query = f'''
    SELECT Week, Month, Income
    FROM IncomeTable
    WHERE Month IN ({','.join(['?'] * len(recent_months))})
'''
cursor.execute(query, recent_months)
rows = cursor.fetchall()

# Store results
Week = []
Month = []
WeekMonth = []
Income = []

for week, month, income in rows:
    Week.append(week)
    Month.append(month)
    WeekMonth.append(f"{week} ({month})")
    Income.append(income)

conn.close()



print(WeekMonth)
print(Income)
# Now you have:
# Week = ["Week 1", "Week 2", ...]
# Month = ["January", "February", ...]
# WeekMonth = ["Week 1 (January)", "Week 2 (February)", ...]
# Income = [520, 590, ...]
