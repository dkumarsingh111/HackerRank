import pandas as pd
import subprocess

# Step 1: Load the Excel sheet
df = pd.read_excel("tables_list.xlsx", sheet_name="Sheet1")
tables = df.iloc[:, 0].tolist()

# Step 2: Loop through each table
for full_table in tables:
    try:
        schema, table = full_table.strip().split(".")

        # Hive command to get DESCRIBE FORMATTED output
        cmd = f"hive -e \"DESCRIBE FORMATTED {schema}.{table};\""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[ERROR] Could not DESCRIBE {full_table}")
            continue

        output = result.stdout

        # Step 3: Extract location and table type
        location = None
        table_type = None

        for line in output.splitlines():
            if "Location:" in line:
                location = line.split("Location:")[1].strip()
            elif "Table Type:" in line:
                table_type = line.split("Table Type:")[1].strip()

        if not location:
            print(f"[WARNING] No HDFS path found for {full_table}")
            continue

        # Step 4: Run HDFS du command
        hdfs_cmd = f"hdfs dfs -du -s -h \"{location}\""
        hdfs_result = subprocess.run(hdfs_cmd, shell=True, capture_output=True, text=True)

        if hdfs_result.returncode != 0:
            print(f"[ERROR] Could not get HDFS size for {full_table}")
            continue

        size_info = hdfs_result.stdout.strip()
        print(f"{full_table:<30} | {table_type:<10} | {size_info}")

    except Exception as e:
        print(f"[EXCEPTION] {full_table}: {e}")
