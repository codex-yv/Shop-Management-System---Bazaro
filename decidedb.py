import sqlite3

# Replace with your actual .db file path
db_file = "Data\\decide.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS TNC (
        EID INTEGER,
        decidee INTEGER
    )
''')
cursor.execute('''
    INSERT INTO TNC (EID, decidee)
    VALUES (?, ?)
''', (1001, 1))

conn.commit()
conn.close()
