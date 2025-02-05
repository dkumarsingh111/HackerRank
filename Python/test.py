import pyodbc
# import struct 

# print(pyodbc.dataSources())
# print(pyodbc.drivers())
# print(struct.calcsize("P") * 8)

conn = None

# conn = pyodbc.connect('DSN=SageLine50v29;UID=Ansuman;PWD=Tissuemed25;Trusted_Connection=yes;')

# conn = pyodbc.connect(
#     r"DRIVER={Sage Line 50 v29};"
#     r"DBQ=C:/Users/10278018/OneDrive - BD/Desktop/ACCDATA/"
# )
try:
    # conn = pyodbc.connect("DRIVER={Sage Line 50 v29};Trusted_Connection=yes;")
    conn = pyodbc.connect('DSN=Sage50;UID=Ansuman;PWD=Tissuemed25;Trusted_Connection=yes;')

    cursor = conn.cursor()
    cursor.execute("SELECT 1")

    # cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
    
    # tables = cursor.fetchall()
    # print("\n🔹 Sage 50 Tables:")
    # for table in tables:
    #     print(table[0])  # Print table name

    print("Connection successful!")
except pyodbc.Error as e:
    print("Database connection error:", e)
finally:
    if conn:
        conn.close()
        print("Connection closed.")