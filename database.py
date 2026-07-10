import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Books Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL
)
""")

# Issued Books Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS issued_books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    roll_no TEXT NOT NULL,
    book_id INTEGER NOT NULL,
    issue_date TEXT NOT NULL,
    return_date TEXT NOT NULL,
    FOREIGN KEY(book_id) REFERENCES books(id)
)
""")

conn.commit()
conn.close()

print("Database Created Successfully!")
