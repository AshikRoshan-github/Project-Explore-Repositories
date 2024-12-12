import psycopg2
import os

def export_tables_to_csv(db_params, schema_name, output_dir):
    """Exports tables from a PostgreSQL schema to CSV files."""
    try:
        conn = psycopg2.connect(**db_params)  # Use dictionary unpacking for cleaner connection
        cursor = conn.cursor()

        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = %s AND table_type = 'BASE TABLE'",
            (schema_name,) # Parameterized query to prevent SQL injection
        )
        tables = cursor.fetchall()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for table_name in tables:  # Simplified loop
            table_name = table_name[0] # Extract table name from tuple. Could also use for table_name, in tables:
            output_file_path = os.path.join(output_dir, f"{table_name}.csv")

            with open(output_file_path, 'w') as output_file:
                cursor.copy_expert( # Use copy_expert for efficiency.  Handles quoting and escaping automatically.
                    f"COPY \"{schema_name}\".\"{table_name}\" TO STDOUT WITH CSV HEADER", output_file
                )
            print(f"Table '{table_name}' exported to '{output_file_path}'")

    except psycopg2.Error as e:
        print(f"Database error: {e}")  # More specific error message
    finally:
        if conn:
            cursor.close() # Close the cursor. Good practice.
            conn.close()



if __name__ == "__main__":
    # Store database parameters in a dictionary
    db_params = {
        "host": "your_host",
        "port": "your_port", # Make sure your port is a string.
        "database": "your_database_name",
        "user": "your_username",
        "password": "your_password"
    }

    schema_name = "your_schema_name"
    output_dir = "D:/csv_exports" # More descriptive output directory name

    export_tables_to_csv(db_params, schema_name, output_dir)
