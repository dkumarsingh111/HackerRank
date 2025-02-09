import pyodbc
import pandas as pd
import warnings
# import struct 

# print(pyodbc.dataSources())
# print(pyodbc.drivers())
# print(struct.calcsize("P") * 8)

warnings.simplefilter(action="ignore", category=UserWarning)

conn = None

try:
    access_db_path = r"C:\DB\sage50db.accdb"

# Connection string for Access (.accdb)
    username = "Ansuman"  # Change to your username
    password = "Tissuemed25"  # Change to your password

    # Connection string for password-protected MS Access (.accdb)
    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        f"DBQ={access_db_path};"
        f"UID={username};"
        f"PWD={password};"
    )

    # Establish Connection
    conn = pyodbc.connect(conn_str)
    # conn = pyodbc.connect('DSN=access50;UID=Ansuman;PWD=Tissuemed25')
    cursor = conn.cursor()

except pyodbc.Error as e:
    print("Sage50Accounts Database connection error:", e)

else:
    try:    
        cursor = conn.cursor()
        tables = cursor.tables()
        print("\nSage50Accounts Tables:")
        
        table_name = 'AUDIT_USAGE'
        output_csv_path = f"C:/DB/Exported_tables/{table_name}.csv"    

        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

        print(df)


    except Exception as e:
        print(f"Error in {table_name} export:", e)
finally:
    if conn:
        conn.close()
        print("Connection closed.")