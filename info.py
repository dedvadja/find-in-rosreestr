# Import sqlite3 module into
# this program as sq
import sqlite3 as sq

# Import pandas module into
# this program as pd
import pandas as pd

# Create a connection object,
# Make a new db if not exist already
# and connect it, if exist then connect.
connection = sq.connect('db/information.db')

# Create a cursor object
curs = connection.cursor()

# Run create table sql query
curs.execute("create table if not exists studentInfo" +
             " (number text, data text, operator text)")

# Load CSV data into Pandas DataFrame
student = pd.read_csv('csv/dannyeLatin.csv')

# Write the data to a sqlite db table
student.to_sql('studentInfo', connection, if_exists='replace', index=True)

# Run select sql query
curs.execute('select * from studentInfo')

# Fetch all records
# as list of tuples
records = curs.fetchall()

# Display result
for row in records:
    # show row
    print(row)

# Close connection to SQLite database
connection.close()