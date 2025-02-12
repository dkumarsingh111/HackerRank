import os
import pyodbc
import warnings
import configparser
import pandas as pd
from datetime import datetime

warnings.simplefilter(action="ignore", category=UserWarning)


current_dir = os.getcwd()
config = configparser.ConfigParser()
config.read(f"{current_dir}/config.ini")

raw_file_path = 'C:/DB/raw_csv_files'

if not os.path.exists(raw_file_path):
    os.makedirs(raw_file_path)

# Access values
db_dsn = config.get("DATABASE", "dsn")
db_user = config.get("DATABASE", "username")
db_pass = config.get("DATABASE", "password")
last_run_date = config.get("SETTINGS", "last_run_date")


try:
    conn = pyodbc.connect(f'DSN={db_dsn};UID={db_user};PWD={db_pass}')

    cursor = conn.cursor()
    tables = [row.table_name for row in cursor.tables(tableType="TABLE")]
    
    print("\nSage50Accounts Tables:")
    for table in tables:
        table_name = table
        output_csv_path = f"{raw_file_path}/{table_name}.csv"            

        try:
            cursor.execute(f"SELECT * FROM {table_name} WHERE 1=0") 
            all_columns = [column[0] for column in cursor.description]

            exclude_columns = []

            selected_columns = [col for col in all_columns if col not in exclude_columns]

            df = pd.read_sql(f'SELECT {', '.join(selected_columns)} FROM {table_name} WHERE RECORD_CREATE_DATE > "{last_run_date}"', conn)
            # df = pd.read_sql(f'SELECT {', '.join(selected_columns)} FROM {table_name}',conn)

            df.to_csv(output_csv_path, index=False)
            print(f"Table '{table_name}' exported to '{output_csv_path}' successfully.")

        except Exception as e:
            print(f"Error in {table_name} table export:", e)


    current_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    config.set("SETTINGS", "last_run_date", current_date)

    with open("config.ini", "w") as configfile:
        config.write(configfile)

    print("Updated 'last_run_date' in SETTINGS section.")

except pyodbc.Error as e:
    print("Sage50Accounts Database connection error:", e)

finally:
    if conn:
        conn.close()
        print("Connection closed.")
        