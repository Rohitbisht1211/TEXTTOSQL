import sqlite3

# ✅ Connect to SQLite database
connection = sqlite3.connect("student.db")
cursor = connection.cursor()

# ✅ Create the table only if it does not exist
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
"""
cursor.execute(table_info)

# ✅ Insert multiple records using executemany() to improve efficiency
students_data = [
    ('Ravi', 'Data Science', 'A', 76),
    ('Sudesh', 'Web Development', 'A', 95),
    ('Kamal', 'DEVOPS', 'A', 62),
    ('Hitesh', 'Web Development', 'A', 45),
    ('Deepak', 'Data Science', 'A', 82)
]

cursor.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?)", students_data)

# ✅ Display all the records
print("The inserted records are:")
data = cursor.execute("SELECT * FROM STUDENT")
for row in data:
    print(row)

# ✅ Commit the transaction and close the connection
connection.commit()
connection.close()
