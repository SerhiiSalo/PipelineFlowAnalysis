import datetime
import pandas as pd
import numpy as np

class Logger:
    """
    Клас для логування повідомлень у файл та на екран з рівнями та часовими мітками.
    """
    def __init__(self, log_file):
        self.log_file = log_file
        with open(self.log_file, 'w') as file:
            file.write("Логування розпочато\n")

    def log(self, message, level="INFO"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        print(log_message)  # Вивід на екран
        with open(self.log_file, 'a') as file:
            file.write(log_message + "\n")