import os
import configparser
from logger import Logger

class ConfigLoader:    
      
    current_dir = os.getcwd()

    @staticmethod  
    def load_config(config_path=f"{current_dir}/config.ini"):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file '{config_path}' not found!")

        config = configparser.ConfigParser()
        config.read(config_path)
        return config
    

    def validate_config(config):
        if "DATABASE" not in config:
            raise Exception("Error: 'DATABASE' section is missing in config.ini!")

        if "dsn" not in config["DATABASE"]:
            raise Exception("Error: 'dsn' key is missing in [DATABASE] section!")
        
        if "username" not in config["DATABASE"]:
            raise Exception("Error: 'username' key is missing in [DATABASE] section!")
        
        if "password" not in config["DATABASE"]:
            raise Exception("Error: 'password' key is missing in [DATABASE] section!")
        
        if "SETTINGS" not in config:
            raise Exception("Error: 'SETTINGS' section is missing in config.ini!")
        
        if "last_run_date" not in config["SETTINGS"]:
            raise Exception("Error: 'last_run_date' key is missing in [SETTINGS] section!")
        
        if "raw_file_path" not in config["SETTINGS"]:
            raise Exception("Error: 'raw_file_path' key is missing in [SETTINGS] section!")
        
        if "TABLES" not in config:
            raise Exception("Error: 'TABLES' section is missing in config.ini!")
        
        if "exclude_columns_list" not in config["TABLES"]:
            raise Exception("Error: 'exclude_columns_list' key is missing in [TABLES] section!")
        
        if "master_tables_list" not in config["TABLES"]:
            raise Exception("Error: 'master_tables_list' key is missing in [TABLES] section!")
