
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
        output_csv_path = f"C:/DB/Exported_tables/AUDIT_USAGE.csv"  
        cursor.execute("SELECT * FROM AUDIT_USAGE WHERE RECORD_CREATE_DATE >= ?")
        


        columns = [column[0] for column in cursor.description]

        batch_size = 1000  # Number of rows per batch

        with open("AUDIT_USAGE.csv", "w", newline="") as file:

            file.write(",".join(columns) + "\n")

            while True:
                rows = cursor.fetchmany(batch_size)
                if not rows:
                    break  # Stop when no more data
                
                df = pd.DataFrame.from_records(rows, columns=columns)
                df.to_csv(file, index=False, header=False, mode="a")  # 

        print("Large dataset exported successfully!")          

        df.to_csv(output_csv_path, index=False)
        print(f"Table AUDIT_USAGE exported to '{output_csv_path}' successfully.")     


    except Exception as e:
        print(f"Error in AUDIT_USAGE export:", e)
finally:
    if conn:
        conn.close()
        print("Connection closed.")