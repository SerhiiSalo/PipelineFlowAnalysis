import os
from DataHandler import DataHandler
from Pipeline import Pipeline
from Visualization import Visualization
from PressureWaveSimulator import PressureWaveSimulator
from Logger import Logger
from EventGenerator import EventGenerator
from enum import Enum
import random

class EventType(Enum):
    ACCIDENT = "accident"
    THEFT = "theft"

# Функція для підготовки середовища
def prepare_environment():
    """
    Підготовка середовища для зберігання даних симуляції.
    """
    if not os.path.exists("Data"):
        os.mkdir("Data")
    else:
        for file in os.listdir("Data"):
            os.remove(os.path.join("Data", file))

# Ініціалізація обробника даних
handler = DataHandler()

# Ініціалізація логера
logger = Logger("simulation_log.txt")

# Ініціалізація моделі трубопроводу
pipeline = Pipeline(
    length=300_000,
    diameter=1.02,
    sensors=[0, 100_000, 250_000, 300_000],
    pressure_norm=34.0,
    flow_rate_norm=3.5
)

# Генерація нормального потоку
pipeline.generate_normal_flow(time_steps=100, noise_level=0.01)
handler.data = pipeline.data
handler.save_data("Data/Pipeline_Normal_Flow.csv")

# Генерація місця події
# Генеруємо випадкові події для різних сценаріїв
random_event_positions = []
for _ in range(5):  # Генеруємо 5 випадкових точок
    event_generator = EventGenerator(pipeline_length=300_000, sensors=pipeline.sensors, min_distance_from_sensors=5000, logger=logger)
    event_position = event_generator.generate_event_position()
    random_event_positions.append(event_position)
    logger.log(f"Згенеровано випадкову подію на позиції: {event_position} м")

# Завантаження даних
handler.load_data("Data/Pipeline_Normal_Flow.csv")

# Додавання аномалій та збереження міток
for event_position in random_event_positions:
    event_type = EventType.ACCIDENT  # Моделюємо лише аварії для навчання
    simulator = PressureWaveSimulator(handler, sensors=[0, 100_000, 250_000, 300_000], wave_speed=1000, pump_positions=[250_000], logger=logger)
    if event_type == EventType.ACCIDENT:
        simulator.apply_long_term_failure(event_position=event_position, pressure_decrease_rate=0.1)
        handler.data.loc[:, "Anomaly"] = handler.data.get("Anomaly", 0)  # Створення стовпця, якщо його немає
        handler.data.loc[event_position, "Anomaly"] = 1
        logger.log(f"Модель аварії завершена для позиції: {event_position} м.")

# Збереження даних у файл
handler.save_data("Data/Pipeline_Event_Simulation.csv")

# Візуалізація
visualizer = Visualization(handler)
visualizer.plot_data(pipeline.sensors)

logger.log("Симуляція завершена.")
