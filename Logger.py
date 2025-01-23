import pandas as pd
import numpy as np

class Logger:
    """
    Клас для логування повідомлень у файл та на екран.
    """
    def __init__(self, log_file):
        self.log_file = log_file
        with open(self.log_file, 'w') as file:
            file.write("Логування розпочато\n")

    def log(self, message):
        print(message)  # Вивід на екран
        with open(self.log_file, 'a') as file:
            file.write(message + "\n")