import sqlite3

# Replace with your actual .db file path
db_file = "Data\\decide.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mongoEarnings (
        EID INTEGER,
        decidee INTEGER
    )
''')
cursor.execute('''
    INSERT INTO mongoEarnings (EID, decidee)
    VALUES (?, ?)
''', (104, 0))

conn.commit()
conn.close()


