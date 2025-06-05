import sqlite3

# Replace with your actual .db file path
db_file = "Data\\decide.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS shopp (
        EID INTEGER,
        binn INTEGER
    )
''')
cursor.execute('''
    INSERT INTO shopp (EID, binn)
    VALUES (?, ?)
''', (203, 1))


cursor.execute('''
    SELECT decidee FROM mongoEarnings WHERE EID = ?
''', (104,))

# result = cursor.fetchone()

# # Check if a record was found
# if result:
#     print("decidee for EID 104 is:", result[0])
# else:
#     print("No record found for EID = 104")

# Commit the changes and close the connection
conn.commit()
conn.close()


