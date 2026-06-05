import sqlite3

conn = sqlite3.connect("resume_data.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS resumes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    resume_name TEXT,

    job_description TEXT,

    score INTEGER

)
""")

conn.commit()
conn.close()

print("Database Created Successfully")