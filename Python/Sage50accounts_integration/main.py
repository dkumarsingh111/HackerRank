import warnings
import pandas as pd
from logger import Logger
from datetime import datetime
from data_fetcher import DataFetcher
from config_loader import ConfigLoader
from database_connector import DatabaseConnector


logger = Logger().get_logger()
warnings.simplefilter(action="ignore", category=UserWarning)


if __name__ == "__main__":
    config = ConfigLoader.load_config()
    ConfigLoader.validate_config(config)
    
    # Initialize database connection
    db_connector = DatabaseConnector(config)
    db_connector.connect()
    
    if db_connector.conn:
        data_fetcher = DataFetcher(db_connector, config)
        data_fetcher.fetch_data()

        #Update last run datetime        
        current_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        config.set("SETTINGS", "last_run_date", current_date)

        with open("config.ini", "w") as configfile:
            config.write(configfile)

        logger.info("Updated 'last_run_date' in SETTINGS section.")        
    
        # Close connection
        db_connector.close_connection()
