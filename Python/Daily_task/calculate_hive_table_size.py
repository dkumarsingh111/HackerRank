import pandas as pd
import jaydebeapi
import subprocess

# ----- CONFIGURATION -----
EXCEL_PATH = "tables_list.xlsx"
HIVE_JDBC_URL = "jdbc:hive2://<hive-host>:10000/default"
HIVE_USER = "your_username"
HIVE_PASSWORD = "your_password"
JDBC_DRIVER_CLASS = "org.apache.hive.jdbc.HiveDriver"
JDBC_JAR_PATH = "/path/to/hive-jdbc-uber.jar"
# --------------------------

# Read table list from Excel
df = pd.read_excel(EXCEL_PATH)
df.columns = ['schema', 'table']  # Expecting two columns: schema and table

# Connect to Hive using JDBC
conn = jaydebeapi.connect(
    JDBC_DRIVER_CLASS,
    HIVE_JDBC_URL,
    [HIVE_USER, HIVE_PASSWORD],
    JDBC_JAR_PATH
)
cursor = conn.cursor()

def get_table_details(schema, table):
    cursor.execute(f"DESCRIBE FORMATTED {schema}.{table}")
    rows = cursor.fetchall()

    location = None
    table_type = None

    for row in rows:
        line = row[0].strip()
        if line.startswith("Location"):
            location = row[1].strip()
        elif line.startswith("Table Type"):
            table_type = row[1].strip()

    return location, table_type

def get_hdfs_size(path):
    try:
        result = subprocess.run(
            ['hdfs', 'dfs', '-du', '-s', '-h', path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().split()[0]  # e.g., "1.2 G"
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Exception: {str(e)}"

# Main execution
print(f"{'Schema.Table':40} {'Type':15} {'Size'}")
print("-" * 70)

for _, row in df.iterrows():
    schema = row['schema']
    table = row['table']
    try:
        location, table_type = get_table_details(schema, table)
        if location:
            size = get_hdfs_size(location)
            print(f"{schema}.{table:30} {table_type:15} {size}")
        else:
            print(f"{schema}.{table:30} Not Found       -")
    except Exception as e:
        print(f"{schema}.{table:30} Error            {str(e)}")

# Cleanup
cursor.close()
conn.close()
