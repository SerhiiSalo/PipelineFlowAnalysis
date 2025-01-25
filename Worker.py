import os
from DataHandler import DataHandler
from Pipeline import Pipeline
from Visualization import Visualization
from PressureWaveSimulator import PressureWaveSimulator
from Logger import Logger
from EventGenerator import EventGenerator
from enum import Enum
import random
import time

class EventType(Enum):
    ACCIDENT = "accident"

class Worker:
    """
    Клас для виконання основних симуляцій та моделювання подій у трубопроводі.
    """
    def __init__(self, logger=None, storage_mode="overwrite"):
        """
        Parameters:
        - logger: Об'єкт для логування.
        - storage_mode: Режим зберігання даних ("overwrite", "append", "separate").
        """
        self.logger = logger if logger else Logger("simulation_log.txt")
        self.sensors = [0, 100_000, 250_000, 300_000]
        self.handler = DataHandler()
        self.pipeline = Pipeline(
            length=300_000,
            diameter=1.02,
            sensors=self.sensors,
            pressure_norm=34.0,
            flow_rate_norm=3.5
        )
        self.storage_mode = storage_mode


    def save_data(self, data, file_name):
        """
        Зберігає дані в залежності від обраного режиму.
        """
        if self.storage_mode == "separate":
            output_path = os.path.join(self.output_folder, file_name)
        else:
            output_path = os.path.join("Data", file_name)
        self.handler.data = data
        self.handler.save_data(output_path)

    def visualize_file(self, file_path):
        """
        Метод для візуалізації даних із заданого файлу.

        Parameters:
        - file_path: шлях до файлу (або повний, або відносний від каталогу Data).
        """
        if not os.path.exists(file_path):
            file_path = os.path.join("Data", file_path)
            if not os.path.exists(file_path):
                self.logger.log(f"Файл {file_path} не знайдено.")
                return

        self.logger.log(f"Завантаження даних із файлу {file_path}...")
        self.handler.load_data(file_path)
        visualizer = Visualization(self.handler)
        visualizer.plot_data(self.sensors)
        self.logger.log(f"Візуалізація завершена для файлу {file_path}.")

    def create_normal_data(self):
        """
        Запуск основної симуляції.
        """
        # Підготовка середовища для збереження
        self.output_folder = DataHandler.prepare_environment(self.storage_mode)
        
        DataHandler.prepare_environment(self.storage_mode)

        # Генерація нормального потоку
        self.logger.log("Генерація нормального потоку...")
        self.pipeline.generate_normal_flow(time_steps=300, noise_level=0.01)
        return self.pipeline.data
    

  

    def run_simulation(self):
        self.handler.data = self.create_normal_data()
        self.save_data(self.handler.data, "Pipeline_Normal_Flow.csv")

        # Генерація події аварії
        self.logger.log("Генерація аварії...")
        while True:
            event_generator = EventGenerator(
                pipeline_length=300_000,
                sensors=self.sensors,
                min_distance_from_sensors=5000,
                logger=self.logger
            )
            event_position = event_generator.generate_event_position()
            if 0 <= event_position <= 300_000:
                self.logger.log(f"Згенеровано єдину подію на позиції: {event_position} м")
                break

        # Визначення випадкового часу аварії
        time_of_event = random.randint(20, 50)
        self.logger.log(f"Час аварії: {time_of_event} секунд.")

        # Моделювання аварії
        simulator = PressureWaveSimulator(
            self.handler,
            sensors=self.sensors,
            wave_speed=1000,
            pump_positions=[250_000],
            logger=self.logger
        )
        simulator.apply_long_term_failure(
            event_position=event_position,
            pressure_decrease_rate=0.1,
            time_of_event=time_of_event
        )

        # Збереження даних у файл
        self.save_data(self.handler.data, "Training_Data.csv")

        # Візуалізація
        visualizer = Visualization(self.handler)
        visualizer.plot_data(self.sensors)

        self.logger.log("Симуляція завершена.")

if __name__ == "__main__":
    worker = Worker(storage_mode="separate")
    #worker.run_simulation()
    worker.visualize_file(file_path="Training_A_20250125_182508_864/Training_Data.csv")
