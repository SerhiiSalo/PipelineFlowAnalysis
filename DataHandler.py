import pandas as pd

class DataHandler:
    """
    Клас для читання та запису даних.
    """
    def __init__(self, file_name=None):
        self.file_name = file_name
        self.data = None

    def save_data(self, file_name):
        """
        Зберігає дані у файл CSV.
        """
        if self.data is not None:
            self.data.to_csv(file_name, index=False)
            print(f"Дані збережено у файл: {file_name}")
        else:
            print("Дані ще не згенеровані.")

    def load_data(self, file_name):
        """
        Завантажує дані з файлу CSV.
        """
        self.data = pd.read_csv(file_name)
        print(f"Дані завантажено з файлу: {file_name}")

    def calculate_deltas(self, sensors, logger):
        """
        Обчислює дельти для кожного сенсора та логує їх.
        """
        if self.data is None:
            print("Дані ще не згенеровані.")
            return

        for sensor in sensors:
            self.data[f"Delta_Pressure_{sensor}m"] = self.data[f"Pressure_{sensor}m"].diff().fillna(0)
            logger.log(f"Дельти для сенсора {sensor} м обчислено.")