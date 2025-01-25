import os
import pandas as pd
import random
import time
from Logger import Logger
from EventGenerator import EventGenerator
from PressureWaveSimulator import PressureWaveSimulator
from Pipeline import Pipeline
from DataHandler import DataHandler

class TrainingDataGenerator:
    """
    Клас для генерації великих наборів даних для навчання моделей аномалій.
    """

    def __init__(self, pipeline_length, sensors, logger=None, storage_mode="separate"):
        """
        Parameters:
        - pipeline_length: довжина трубопроводу (метри).
        - sensors: позиції сенсорів (метри).
        - logger: об'єкт для логування (необов'язковий).
        - storage_mode: режим зберігання даних ("overwrite", "append", "separate").
        """
        self.pipeline_length = pipeline_length
        self.sensors = sensors
        self.logger = logger if logger else Logger("training_data_log.txt")
        self.storage_mode = storage_mode
        self.handler = DataHandler()
        self.pipeline = Pipeline(
            length=pipeline_length,
            diameter=1.02,
            sensors=sensors,
            pressure_norm=34.0,
            flow_rate_norm=3.5
        )


    def save_data(self, file_name):
        """
        Зберігає дані в залежності від обраного режиму.
        """
        if self.storage_mode == "separate":
            output_path = os.path.join(self.output_folder, file_name)
        else:
            output_path = os.path.join("Data", file_name)

        if self.storage_mode == "append" and os.path.exists(output_path):
            existing_data = pd.read_csv(output_path)
            combined_data = pd.concat([existing_data, self.handler.data], ignore_index=True)
            combined_data.to_csv(output_path, index=False)
        else:
            self.handler.save_data(output_path)

    def generate_training_data(self, total_steps, anomaly_ratio=0.2):
        """
        Генерує навчальний набір даних із нормальними та аномальними сценаріями.

        Parameters:
        - total_steps: загальна кількість часових кроків.
        - anomaly_ratio: частка даних з аномаліями (від 0 до 1).
        """
        self.logger.log("Початок генерації навчальних даних...")

        # Генерація нормального потоку
        self.output_folder = DataHandler.prepare_environment(self.storage_mode)  # Папка для нормальних даних
        normal_steps = int(total_steps * (1 - anomaly_ratio))
        self.logger.log(f"Генерація {normal_steps} нормальних часових кроків...")
        self.pipeline.generate_normal_flow(time_steps=normal_steps, noise_level=0.01)
        self.handler.data = self.pipeline.data
        self.save_data("Training_Data.csv")

        # Генерація аномальних даних
        anomaly_steps = total_steps - normal_steps
        self.logger.log(f"Генерація {anomaly_steps} аномальних часових кроків...")

        for _ in range(anomaly_steps):
            # Створення окремої папки для кожної аномальної події
            self.output_folder = DataHandler.prepare_environment(self.storage_mode)
            
            event_generator = EventGenerator(
                pipeline_length=self.pipeline_length,
                sensors=self.sensors,
                min_distance_from_sensors=5000,
                logger=self.logger
            )
            event_position = event_generator.generate_event_position()
            time_of_event = random.randint(20, 50)

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
            self.save_data("Training_Data.csv")

        self.logger.log("Навчальні дані згенеровано.")



if __name__ == "__main__":
    logger = Logger("training_data_log.txt")
    sensors = [0, 100_000, 250_000, 300_000]
    generator = TrainingDataGenerator(pipeline_length=300_000, sensors=sensors, logger=logger, storage_mode="append")
    generator.generate_training_data(total_steps=10000, anomaly_ratio=0.2)
