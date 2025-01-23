from DataHandler import DataHandler
from TheftEvent import TheftEvent
from Event import Event
from Pipeline import Pipeline
from Visualization import Visualization
from PressureWaveSimulator import PressureWaveSimulator
from Logger import Logger
from EventGenerator import EventGenerator
from enum import Enum

class EventType(Enum):
    ACCIDENT = "accident"
    THEFT = "theft"





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
handler.save_data("Pipeline_Normal_Flow.csv")

# Генерація місця події
event_generator = EventGenerator(pipeline_length=300_000, sensors=pipeline.sensors, min_distance_from_sensors=5000, logger=logger)
event_position = event_generator.generate_event_position()

# Завантаження даних
handler.load_data("Pipeline_Normal_Flow.csv")

# Вибір типу події
event_type = EventType.ACCIDENT

simulator = PressureWaveSimulator(handler, sensors=[0, 100_000, 250_000, 300_000], wave_speed=1000, pump_positions=[250_000], logger=logger)

if event_type == EventType.ACCIDENT:
    simulator.apply_long_term_failure(event_position=event_position, pressure_decrease_rate=0.1)
elif event_type == EventType.THEFT:
    simulator.apply_pressure_wave(event_position=event_position, pressure_increase=5)

handler.save_data("Pipeline_Event_Simulation.csv")

# Візуалізація
visualizer = Visualization(handler)
visualizer.plot_data(pipeline.sensors)

logger.log("Симуляція завершена.")
