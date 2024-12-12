import pyodbc
import json

db_dict = {}

# Replace the placeholders with your server, database, username, and password
server   = 'xxx'
database = 'xxx'
username = 'xxx'
password = 'xxx'

# Create the connection string
conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Establish the connection
conn = pyodbc.connect(conn_str)

# Create a cursor
cursor = conn.cursor()

# Query to get all table names
table_query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"

# Execute the query
cursor.execute(table_query)

# Fetch all the table names and save them in a list
table_names = [row.TABLE_NAME for row in cursor]

for table_name in table_names:
    # Parameterize the table name to avoid SQL injection
    column_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?"
    cursor.execute(column_query, (table_name,))
    column_names = [row.COLUMN_NAME for row in cursor]
    db_dict[table_name] = column_names

# Convert the dictionary to JSON string with indentation
json_str = json.dumps(db_dict, indent=4)

with open(r'D:\JIFFY_PROJECT\Json_file\table_names_json.txt','w') as file:
    file.write(json_str)

# Close the cursor and connection
cursor.close()
conn.close()
