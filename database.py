import sqlite3

# Connect Database
conn = sqlite3.connect("resume_data.db")

# Create Cursor
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS resumes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    resume_name TEXT,

    job_description TEXT,

    score INTEGER
)
""")

conn.commit()

print("Database Created Successfully")