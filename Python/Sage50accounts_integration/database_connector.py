import pyodbc
from logger import Logger


class DatabaseConnector:
    def __init__(self, config):
        self.db_dsn = config.get("DATABASE", "dsn")
        self.db_user = config.get("DATABASE", "username")
        self.db_pass = config.get("DATABASE", "password")
        self.conn = None
        self.logger = Logger().get_logger()

    def connect(self):
        try:
            self.conn = pyodbc.connect(f'DSN={self.db_dsn};UID={self.db_user};PWD={self.db_pass}')
            self.logger.info("Database connection established successfully.")
        except pyodbc.Error as e:
            self.logger.error(f"Sage50Accounts Database connection error: {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed.")