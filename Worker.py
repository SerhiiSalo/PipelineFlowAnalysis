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
pipeline.generate_normal_flow(time_steps=300, noise_level=0.01)
handler.data = pipeline.data
handler.save_data("Data/Pipeline_Normal_Flow.csv")

# Генерація єдиної події - аварії
# Генеруємо одну випадкову точку для аварії
while True:
    event_generator = EventGenerator(pipeline_length=300_000, sensors=pipeline.sensors, min_distance_from_sensors=5000, logger=logger)
    event_position = event_generator.generate_event_position()
    if 0 <= event_position <= 300_000:
        logger.log(f"Згенеровано єдину подію на позиції: {event_position} м")
        break

# Визначення випадкового часу аварії
time_of_event = random.randint(20, 50)  # Аварія виникає між 20 і 50 секундами
logger.log(f"Час аварії: {time_of_event} секунд.")

# Завантаження даних
handler.load_data("Data/Pipeline_Normal_Flow.csv")

# Моделювання аварії
simulator = PressureWaveSimulator(handler, sensors=[0, 100_000, 250_000, 300_000], wave_speed=1000, pump_positions=[250_000], logger=logger)
simulator.apply_long_term_failure(event_position=event_position, pressure_decrease_rate=0.1, time_of_event=time_of_event)
logger.log(f"Аварія додана на позиції: {event_position} м.")

# Збереження даних у файл
handler.save_data("Data/Pipeline_Event_Simulation.csv")

# Візуалізація
visualizer = Visualization(handler)
visualizer.plot_data(pipeline.sensors)

logger.log("Симуляція завершена.")
