The Python script performs incremental data loading from SQL Server to Snowflake. 

Here's an architectural breakdown:

**1. Initialization and Logging:**

Process:

Imports necessary libraries (pyodbc, pandas, python-dotenv, snowflake-snowpark, os, logging).

Sets up logging to a file named after the source table.

Clears or creates the log file.

Retrieves the last run timestamp (Lst_RunTime) from the .env file.

**2. Data Extraction from SQL Server:**

Input: Connection details for SQL Server, src_table name, Lst_RunTime.

Process:

Establishes a connection to SQL Server using pyodbc.

Executes a SQL query to select data from src_table where SYNCSTARTDATETIME is greater than Lst_RunTime. Uses parameterized queries for security.

Loads the retrieved data into a Pandas DataFrame.

Adds a new column SF_INSERT_TIMESTAMP with the current timestamp.

Updates the Lst_RunTime in the .env file with the maximum SYNCSTARTDATETIME from the extracted data if the DataFrame is not empty and new_runtime is not NaT.

Output: Pandas DataFrame (df) containing the new data.

**3. Data Loading to Snowflake:**

Input: Pandas DataFrame (df), Snowflake connection parameters, stg_table name.

Process:

Creates a Snowpark session to connect to Snowflake.

Converts the Pandas DataFrame to a Snowpark DataFrame.

Loads the Snowpark DataFrame into the stg_table using save_as_table in append mode.

Output: Data loaded into the Snowflake staging table.

**4. Cleanup:**

Process: Closes the SQL Server and Snowflake connections and the logging handler.

Architecture Diagram:

![image](https://github.com/user-attachments/assets/7f9522aa-44d4-4aa0-bc99-f379e50b6fb6)

**Script:** 

import pyodbc
import pandas as pd
from dotenv import load_dotenv, set_key
from datetime import datetime
from snowflake.snowpark import Session
import os
import logging

# Get the current timestamp
current_timestamp = datetime.now()

# Define the source table in Snowflake
src_table= 'EmployeeRecords'

# Define the staging table in Snowflake
stg_table = "STG_EMPLOYEERECORDS"

log_file_path = f'{src_table}.log'

# Check if the log file exists
if os.path.exists(log_file_path):
    with open(log_file_path, 'w') as file:
        # Clearing the file by writing nothing to it
        pass
    print(f"{log_file_path} has been cleared.")
else:
    print(f"{log_file_path} does not exist. Skipping clearing.")

# Proceed with the rest of the code
print("Continuing with the rest of the script...")


# Configure logging
log_filename = f'{src_table}.log'
logging.basicConfig(filename=log_filename,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load the .env file
load_dotenv()

# Retrieve the current Lst_RunTime from .env file
current_lifetime = os.getenv('Lst_RunTime')
logging.info(f'Current Lst_RunTime: {current_lifetime}')

try:
    # Convert the retrieved time to a datetime object
    Lst_RunTime = datetime.strptime(current_lifetime, '%Y-%m-%d %H:%M:%S.%f')
except Exception as e:
    logging.error(f"Error converting Lst_RunTime to datetime: {e}")
    raise

# Define the connection parameters for SQL Server
server = 'xxx'  # Add your server name
database = 'xxx'
username = 'xxx'
password = 'xxx'

# Create the connection string for pyodbc
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Establish the connection using pyodbc
try:
    connection = pyodbc.connect(connection_string)
    logging.info("Connection to SQL Server successful!")
except Exception as e:
    logging.error(f"Error while connecting to SQL Server: {e}")
    connection = None

if connection:
    # SQL query to select all data from the table where SYNCSTARTDATETIME is greater than Lst_RunTime
    query = f"SELECT * FROM {src_table} WHERE SYNCSTARTDATETIME > ?"

    # Load the data into a pandas DataFrame using pyodbc
    try:
        # Execute the query with a parameterized SQL statement using pyodbc
        cursor = connection.cursor()
        cursor.execute(query, (Lst_RunTime,))
        
        # Fetch all the rows from the query result
        rows = cursor.fetchall()
        
        # Get the column names from the cursor description
        columns = [column[0].upper() for column in cursor.description]

        logging.info(f"Columns retrieved: {columns}")
        
        # Load the data into a pandas DataFrame
        df = pd.DataFrame.from_records(rows, columns=columns)

        logging.info(f"Data loaded into DataFrame successfully with {len(df)} records.")

        df['SF_INSERT_TIMESTAMP'] = current_timestamp

        logging.info(f"SF_INSERT_TIMESTAMP implemented successfully to the dataframe.")

        # Convert to datetime (ensure the column exists in df)
        if 'SYNCSTARTDATETIME' in df.columns:
            df['SYNCSTARTDATETIME'] = pd.to_datetime(df['SYNCSTARTDATETIME'])

        # Check if the DataFrame is empty
        if not df.empty:
            # Find the maximum value of SYNCSTARTDATETIME
            new_runtime = df['SYNCSTARTDATETIME'].max()

            # Only update .env if new_runtime is not NaT
            if pd.notna(new_runtime):
                # Update the .env file with the new Lst_RunTime
                dotenv_path = '.env'
                set_key(dotenv_path, 'Lst_RunTime', new_runtime.strftime('%Y-%m-%d %H:%M:%S.%f'))

                logging.info(f"New Lst_RunTime set in .env: {new_runtime}")
            else:
                logging.warning("New Lst_RunTime is NaT, not updating .env.")
        else:
            logging.info("No new records found.")

    except Exception as e:
        logging.error(f"Error while executing SQL query: {e}")
    finally:
        cursor.close()
        connection.close()
        logging.info("SQL Server connection closed.")

# Now, let's set up the Snowflake Snowpark session
    snowflake_connection_parameters = {
        "account": 'xxx',
        "user": 'xxx',
        "password": 'xxx',
        "role": 'xxx',
        "warehouse": 'xxx',
        "database": 'xxx',
        "schema": 'xxx'
    }

    try:
        # Create a Snowflake Snowpark session
        session = Session.builder.configs(snowflake_connection_parameters).create()
        logging.info("Snowpark session created successfully!")

        # Convert the pandas DataFrame to a Snowpark DataFrame
        snowpark_df = session.create_dataframe(df)

        # Insert the data into the Snowflake table
        if not df.empty:
            try:
                # Use save_as_table to insert data into the Snowflake table
                snowpark_df.write.save_as_table(stg_table, mode="append")
                logging.info(f"Data inserted successfully into {stg_table}.")
            except Exception as e:
                logging.error(f"Error while inserting data into Snowflake: {e}")
        else:
            logging.info(f"No data to insert into {stg_table}.")

    except Exception as e:
        logging.error(f"Error while creating Snowflake session: {e}")
    
    finally:
        # Close the Snowpark session after completion
        if session:
            session.close()
            logging.info("Snowpark session closed.")

print("----------CHECK THE LOG-----------")

