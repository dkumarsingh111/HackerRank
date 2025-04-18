import os
import pandas as pd
from logger import Logger

class DataFetcher:
    def __init__(self, connector, config):
        self.connector = connector
        self.logger = Logger().get_logger()
        self.raw_file_path = config.get("SETTINGS", "raw_file_path")
        self.last_run_date = config.get("SETTINGS", "last_run_date")
        self.master_tables = config.get("TABLES","master_tables_list")
        self.exclude_columns = config.get("TABLES","exclude_columns_list")


    def fetch_data(self):

        if not os.path.exists(self.raw_file_path):
            os.makedirs(self.raw_file_path)

        cursor = self.connector.conn.cursor()
        tables = [row.table_name for row in cursor.tables(tableType="TABLE")]
        transationTables = [table for table in tables if table not in self.master_tables]
       
        
        #Incremental Data Load
        for table in transationTables:
            output_csv_path = f"{self.raw_file_path}/{table}.csv"            

            try:
                cursor.execute(f"SELECT * FROM {table} WHERE 1=0") 
                all_columns = [column[0] for column in cursor.description]

                selected_columns = [col for col in all_columns if col not in self.exclude_columns]

                df = pd.read_sql(f'SELECT {', '.join(selected_columns)} FROM {table} WHERE RECORD_CREATE_DATE > "{self.last_run_date}"', self.connector.conn)

                df.to_csv(output_csv_path, index=False)
                self.logger.info(f"Table '{table}' exported to '{output_csv_path}' successfully.")

            except Exception as e:
                self.logger.error(f"Error in {table} table export: {e}")



        #Full Data Load
        for table in self.master_tables:
            output_csv_path = f"{self.raw_file_path}/{table}.csv"            

            try:
                cursor.execute(f"SELECT * FROM {table} WHERE 1=0") 
                all_columns = [column[0] for column in cursor.description]

                selected_columns = [col for col in all_columns if col not in self.exclude_columns]

                df = pd.read_sql(f'SELECT {', '.join(selected_columns)} FROM {table}', self.connector.conn)

                df.to_csv(output_csv_path, index=False)
                self.logger.info(f"Table '{table}' exported to '{output_csv_path}' successfully.")

            except Exception as e:
                self.logger.error(f"Error in {table} table export: {e}")
