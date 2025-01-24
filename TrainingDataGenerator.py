import os
import random
from DataHandler import DataHandler
from Pipeline import Pipeline
from PressureWaveSimulator import PressureWaveSimulator
from Logger import Logger
from EventGenerator import EventGenerator
from Visualization import Visualization
from enum import Enum

class EventType(Enum):
    ACCIDENT = "accident"

class TrainingDataGenerator:
    """
    Клас для генерації великих наборів даних для навчання моделей аномалій.
    """

    def __init__(self, pipeline_length, sensors, logger=None):
        """
        Parameters:
        - pipeline_length: довжина трубопроводу (метри).
        - sensors: позиції сенсорів (метри).
        - logger: об'єкт для логування (необов'язковий).
        """
        self.pipeline_length = pipeline_length
        self.sensors = sensors
        self.logger = logger if logger else Logger("training_data_log.txt")
        self.handler = DataHandler()
        self.pipeline = Pipeline(
            length=pipeline_length,
            diameter=1.02,
            sensors=sensors,
            pressure_norm=34.0,
            flow_rate_norm=3.5
        )

    def prepare_environment(self):
        """
        Підготовка середовища для зберігання даних симуляції.
        """
        if not os.path.exists("Data"):
            os.mkdir("Data")
        else:
            for file in os.listdir("Data"):
                os.remove(os.path.join("Data", file))

    def generate_training_data(self, total_steps, anomaly_ratio=0.2):
        """
        Генерує навчальний набір даних із нормальними та аномальними сценаріями.

        Parameters:
        - total_steps: загальна кількість часових кроків.
        - anomaly_ratio: частка даних з аномаліями (від 0 до 1).
        """
        self.logger.log("Початок генерації навчальних даних...")

        # Генерація нормального потоку
        normal_steps = int(total_steps * (1 - anomaly_ratio))
        self.logger.log(f"Генерація {normal_steps} нормальних часових кроків...")
        self.pipeline.generate_normal_flow(time_steps=normal_steps, noise_level=0.01)
        self.handler.data = self.pipeline.data

        # Генерація аномальних даних
        anomaly_steps = total_steps - normal_steps
        self.logger.log(f"Генерація {anomaly_steps} аномальних часових кроків...")

        for _ in range(anomaly_steps):
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

        # Збереження результатів
        output_file = "Data/Training_Data.csv"
        self.handler.save_data(output_file)
        self.logger.log(f"Навчальні дані збережено у файл: {output_file}")

if __name__ == "__main__":
    logger = Logger("training_data_log.txt")
    sensors = [0, 100_000, 250_000, 300_000]
    generator = TrainingDataGenerator(pipeline_length=300_000, sensors=sensors, logger=logger)
    generator.prepare_environment()
    generator.generate_training_data(total_steps=10000, anomaly_ratio=0.2)
