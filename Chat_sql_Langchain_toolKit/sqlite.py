import sqlite3

## Connect to SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect("student.db")

## Create a cursor object to execute SQL commands
cursor = connection.cursor()

## Create the table (if not exists)
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(50),
    CLASS VARCHAR(50),
    SECTION VARCHAR(5),
    MARKS INT
)
"""

cursor.execute(table_info)

## Insert the updated records
cursor.execute("""INSERT INTO STUDENT VALUES ('Rahul Sharma', 'Data Science', 'A', 85)""")
cursor.execute("""INSERT INTO STUDENT VALUES ('Priya Singh', 'Machine Learning', 'B', 92)""")
cursor.execute("""INSERT INTO STUDENT VALUES ('Amit Verma', 'DevOps', 'A', 78)""")
cursor.execute("""INSERT INTO STUDENT VALUES ('Sneha Roy', 'Cybersecurity', 'C', 88)""")
cursor.execute("""INSERT INTO STUDENT VALUES ('Arjun Patil', 'Data Science', 'B', 74)""")
cursor.execute("""INSERT INTO STUDENT VALUES ('Neha Gupta', 'Machine Learning', 'A', 90)""")
cursor.execute("""INSERT INTO STUDENT VALUES ('Rohan Joshi', 'DevOps', 'C', 82)""")
cursor.execute("""INSERT INTO STUDENT VALUES ('Pooja Shah', 'Cybersecurity', 'B', 89)""")
cursor.execute("""INSERT INTO STUDENT VALUES ('Karan Mehta', 'Data Science', 'A', 76)""")
cursor.execute("""INSERT INTO STUDENT VALUES ('Simran Kaur', 'Machine Learning', 'B', 94)""")

## Display all the records
print("The inserted records are:")
data = cursor.execute("SELECT * FROM STUDENT")
for row in data:
    print(row)

## Commit the changes and close the connection
connection.commit()
connection.close()
