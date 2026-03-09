import os
import logging
from datetime import datetime
import structlog

class CustomLogger:
    def __init__(self, log_dir="logs"):
        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)
        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        self.log_file_path = os.path.join(self.logs_dir, log_file)

    def get_logger(self, name=__file__):# this method will be used to get the logger for the code of the current .py file from which we will call this method. By default, the name will be the complete path of the current .py file.
        logger_name = os.path.basename(name)#extracts the file name from the path.

        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[console_handler, file_handler]
        )

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(), #logger factory acts as bridge between structlog and python logger. structlog takes the user input (to be logged) and converts it to json and gives it to LoggerFactory which gives that JSON to the python logger so that it can give this format to its file and console handlers.
            cache_logger_on_first_use=True,# when the get logger method is first called, it will create a logger object and cache it so that next time when we call the get logger method, it will return the cached logger object instead of creating a new one. so whenever we call the get_logger() with the same module(or app) name, the logger object that has been created initially will be used to perform all the subsequent operations in that get_logger() method.
        )

        return structlog.get_logger(logger_name)
