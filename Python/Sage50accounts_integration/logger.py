import os
import logging

class Logger:

    current_dir = os.getcwd()
    if not os.path.exists(f"{current_dir}/logs"):
            os.makedirs(f"{current_dir}/logs")

    def __init__(self, log_file=f"{current_dir}/logs/app.log"):
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger("AppLogger")

    def get_logger(self):
        return self.logger