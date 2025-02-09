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
        tables = cursor.tables()
        print("\nSage50Accounts Tables:")
        # for table in tables:
            # table_name = table.table_name
        table_name = "PREPAYMENT"
        output_csv_path = f"C:/DB/Exported_tables/{table_name}.csv"            

        # if table_name != "AUDIT_USAGE" and table_name != "PREPAYMENT":
        df = pd.DataFrame(pd.read_sql(f"SELECT NAME, NOMINAL_CODE_1, NOMINAL_CODE_2, AMOUNT, MONTHS_TO_POST, MONTHS_POSTED, DEPT_NUMBER, DEPT_NAME, CStr(RECORD_CREATE_DATE) FROM {table_name}", conn))

        df.to_csv(output_csv_path, index=False)
        print(f"Table '{table_name}' exported to '{output_csv_path}' successfully.")     


    except Exception as e:
        print(f"Error in {table_name} export:", e)
finally:
    if conn:
        conn.close()
        print("Connection closed.")