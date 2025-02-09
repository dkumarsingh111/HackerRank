
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
    conn = pyodbc.connect('DSN=Sage50;UID=Ansuman;PWD=Tissuemed25')

except pyodbc.Error as e:
    print("Sage50Accounts Database connection error:", e)

else:
    try:    

        cursor = conn.cursor()
        table_name = "PREPAYMENT"
        cursor.execute(f"SELECT TOP 5 * FROM {table_name} WHERE RECORD_CREATE_DATE >= '2006-07-01'")  # Fetch only 5 rows

        columns = [column[0] for column in cursor.description]

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert to pandas DataFrame
        df = pd.DataFrame.from_records(rows, columns=columns)  

        print(df)


        # cursor = conn.cursor()
        # tables = cursor.tables()
        # print("\nSage50Accounts Tables:")
        # for table in tables:
        #     table_name = table.table_name
        output_csv_path = f"C:/DB/Exported_tables/{table_name}.csv"            

        #     # df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        #     query = "SELECT * FROM AUDIT_USAGE"
        #     df = pd.read_sql(query, conn)
        #     print("hello")

        df.to_csv(output_csv_path, index=False)
        print(f"Table '{table_name}' exported to '{output_csv_path}' successfully.")     


    except Exception as e:
        print(f"Error in {table_name} export:", e)
finally:
    if conn:
        conn.close()
        print("Connection closed.")