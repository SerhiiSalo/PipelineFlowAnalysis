import pandas as pd
import numpy as np
from Logger import Logger
import random

class PressureWaveSimulator:
    """
    Клас для моделювання поширення сплесків тиску в трубопроводі та моделювання аварійних подій.
    """

    def __init__(self, data_handler, sensors, wave_speed, pump_positions, logger, gradual_pressure_drop=False):
        """
        Parameters:
        - data_handler: обробник даних трубопроводу.
        - sensors: список сенсорів (позиції в метрах).
        - wave_speed: швидкість поширення хвилі (м/с).
        - pump_positions: позиції насосів (метри).
        - logger: об'єкт для логування.
        - gradual_pressure_drop: чи застосовувати плавне падіння тиску (True) або миттєве (False).
        """
        self.data_handler = data_handler
        self.sensors = sensors
        self.wave_speed = wave_speed
        self.pump_positions = pump_positions
        self.logger = logger
        self.gradual_pressure_drop = gradual_pressure_drop

    def apply_long_term_failure(self, event_position, pressure_decrease_rate, time_of_event):
        """
        Моделює довготривалу аварію з падінням тиску.
        
        Parameters:
        - event_position: позиція аварії (у метрах).
        - pressure_decrease_rate: швидкість падіння тиску (атм за одиницю часу).
        - time_of_event: час початку аварії (у секундах).
        """
        self.logger.log(f"Довготривала аварія виявлена на {event_position} м. Час події: {time_of_event} секунд.")

        time_steps = len(self.data_handler.data)
        for sensor in self.sensors:
            distance = abs(event_position - sensor)
            time_delay = int(distance / self.wave_speed)
            start_time = time_of_event + time_delay

            if start_time < time_steps:
                self.logger.log(f"Хвиля аварії досягає сенсора на {sensor} м через {time_delay} секунд (загальний час: {start_time} секунд).")
                
                # Розрахунок дельти тиску в момент аварії
                initial_pressure = self.data_handler.data.loc[start_time, f"Pressure_{sensor}m"]
                new_pressure = max(0, initial_pressure - pressure_decrease_rate)
                pressure_delta = initial_pressure - new_pressure

                for t in range(start_time, time_steps):
                    # Віднімання дельти від поточного значення
                    self.data_handler.data.loc[t, f"Pressure_{sensor}m"] -= pressure_delta
