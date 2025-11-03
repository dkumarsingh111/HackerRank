import pandas as pd
import jaydebeapi
import subprocess

# ----- CONFIGURATION -----
CSV_READ_PATH = "hive_tables_list.csv"
CSV_WRITE_PATH = "hive_tables_loc_list.csv"
HIVE_JDBC_URL = "jdbc:hive2://prd00-hdi00-spark-int.azurehdinsight.net:443/default;transportMode=http;ssl=true;httpPath=/hive2"
HIVE_USER = "admin"
HIVE_PASSWORD = "P@$$w0rd"
JDBC_DRIVER_CLASS = "org.apache.hive.jdbc.HiveDriver"
JDBC_JAR_PATH = "hive-jdbc-uber-2.6.5.0-292.jar"

# --------------------------

# Read table list from Excel
df = pd.read_csv(CSV_READ_PATH)
df = df[df['Table_Name'].notna()]
df['Table_Name'] = df['Table_Name'].str.strip()
df = df[df['Table_Name'].str.contains(r'\.')]

# Split schema.table into two separate columns
df[['schema', 'table']] = df['Table_Name'].str.split('.', n=1, expand=True)

# Optional: Show result
print(df[['schema', 'table']])

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
        cmd = f'hdfs dfs -du -s -h "{path}"'
        print(cmd)
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"result: {result}")
        if result.returncode == 0:
            return result.stdout.strip().split()[0]  # e.g., "1.2 G"
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Exception: {str(e)}"

# Main execution
# print(f"{'Schema.Table':50} {'Type':20} {'Location'}")
print(f"{'Schema.Table':50} {'Type':20} {'size':20} {'Location'}")
print("-" * 70)

for _, row in df.iterrows():
    schema = row['schema']
    table = row['table']
    try:
        location, table_type = get_table_details(schema, table)
        i=1
        if location:
            # size = get_hdfs_size(location)
            # print(f"{schema}.{table:40} {table_type:20} {size:20} {location}")
            print(f"{schema}.{table:40} {table_type:20} {location}")

            # with open(f"{CSV_WRITE_PATH}", "a") as file:
            #     model_name = file.write(f"{schema}.{table},{table_type},{location},{f'hdfs dfs -du -s -h "{location}"'}")
        else:
            print(f"{schema}.{table:40} Not Found       -")
    except Exception as e:
        print(f"{schema}.{table:40} Error            {str(e)}")

# Cleanup
cursor.close()
conn.close()
