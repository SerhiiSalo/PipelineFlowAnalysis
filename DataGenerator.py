import pandas as pd
import numpy as np

# Константи для генерації даних
D = 1.02  # Діаметр труби у метрах
rho = 850  # Густина нафти в кг/м³
A = np.pi * (D ** 2) / 4  # Площа перерізу труби у м²

PRESSURE_NORM = 34.0  # Нормальний тиск (атм)
FLOW_RATE_NORM = 3.5  # Нормальна витрата (м³/с)
NOISE_LEVEL = 0.02  # Рівень шуму

class SimulationDataGenerator:
    """
    Клас для генерації даних трубопроводу з можливістю додавання аварій.
    """

    def __init__(self):
        self.data = None

    def generate_data(self, time_steps, sensors, include_failure=False, include_theft=False):
        """
        Генерує дані трубопроводу.

        Parameters:
        - time_steps (int): Кількість часових кроків.
        - sensors (list): Позиції сенсорів.
        - include_failure (bool): Чи включати аварії.
        - include_theft (bool): Чи включати крадіжки.
        """
        self.generate_normal_flow(time_steps, sensors)
        if include_failure or include_theft:
            self.add_anomalies(sensors)

    def generate_normal_flow(self, time_steps, sensors):
        """
        Генерує нормальні дані потоку.

        Parameters:
        - time_steps (int): Кількість часових кроків.
        - sensors (list): Позиції сенсорів.
        """
        data = {
            "Time": np.arange(time_steps),
            "Anomaly": [0] * time_steps
        }
        for sensor in sensors:
            data[f"Pressure_{sensor}m"] = 34.0 + np.random.uniform(-0.02, 0.02, time_steps)
            data[f"FlowRate_{sensor}m"] = 3.5 + np.random.uniform(-0.02, 0.02, time_steps)

        self.data = pd.DataFrame(data)

    def add_anomalies(self, sensors):
        """
        Додає аномалії до даних.

        Parameters:
        - sensors (list): Список позицій сенсорів.
        """
        anomaly_index = len(self.data) // 3
        self.data.loc[anomaly_index, f"Pressure_{sensors[1]}m"] -= 5
        self.data.loc[anomaly_index, "Anomaly"] = 1

    def save_data(self, file_path):
        """
        Зберігає дані у файл CSV.

        Parameters:
        - file_path (str): Шлях до файлу.
        """
        self.data.to_csv(file_path, index=False)
        print(f"Дані збережено у файл {file_path}")
