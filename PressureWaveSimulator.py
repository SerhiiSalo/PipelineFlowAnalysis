import pandas as pd
import numpy as np

class PressureWaveSimulator:
    """
    Клас для моделювання поширення сплесків тиску в трубопроводі та моделювання аварійних подій.
    """

    def __init__(self, data_handler, sensors, wave_speed, pump_positions, logger):
        """
        Ініціалізація об'єкта PressureWaveSimulator.

        Parameters:
        - data_handler: Об'єкт DataHandler для роботи з даними.
        - sensors (list): Список позицій сенсорів уздовж трубопроводу.
        - wave_speed (float): Швидкість поширення хвилі тиску (м/с).
        - pump_positions (list): Позиції насосів у метрах.
        - logger: Об'єкт Logger для запису логів.
        """
        self.data_handler = data_handler  # Обробник даних для роботи з поточними даними
        self.sensors = sensors  # Позиції сенсорів на трубопроводі
        self.wave_speed = wave_speed  # Швидкість поширення хвилі тиску
        self.pump_positions = pump_positions  # Позиції насосів
        self.logger = logger  # Логер для запису подій

    def apply_pressure_wave(self, event_position, pressure_increase):
        """
        Моделює поширення сплеску тиску між сенсорами.

        Parameters:
        - event_position: позиція сплеску (у метрах).
        - pressure_increase: величина сплеску тиску.
        """
        time_steps = len(self.data_handler.data)

        for sensor in self.sensors:
            distance = abs(event_position - sensor)
            time_delay = distance / self.wave_speed  # Час затримки у секундах

            # Визначення сегменту труби
            segment = f"між {min(event_position, sensor)} м і {max(event_position, sensor)} м"

            # Якщо є насос на шляху, хвиля не поширюється далі
            if any(pump <= max(event_position, sensor) and pump >= min(event_position, sensor) for pump in self.pump_positions):
                self.logger.log(f"Сплеск зупинено насосом на сегменті {segment}.")
                continue

            # Визначаємо найближчий крок часу для затримки
            time_index = int(time_delay)
            if time_index < time_steps:
                self.logger.log(f"Сплеск тиску на {pressure_increase} атм досягає сенсора {sensor} м через {time_delay:.2f} секунд на сегменті {segment}.")
                if f"Pressure_{sensor}m" in self.data_handler.data.columns:
                    self.data_handler.data.loc[time_index, f"Pressure_{sensor}m"] += pressure_increase

                    # Додатково впливаємо на витрату на відповідному сенсорі
                    self.data_handler.data.loc[time_index, f"FlowRate_{sensor}m"] += pressure_increase * 0.01

    def apply_long_term_failure(self, event_position, pressure_decrease_rate):
        """
        Моделює довготривалу аварію з поступовим падінням тиску.

        Parameters:
        - event_position: позиція аварії (у метрах).
        - pressure_decrease_rate: швидкість падіння тиску (атм за одиницю часу).
        """
        # Ресет індексів для забезпечення послідовності
        self.data_handler.data.reset_index(drop=True, inplace=True)
        time_steps = len(self.data_handler.data)
        self.logger.log(f"Довготривала аварія виявлена на {event_position} м.")

        for sensor in self.sensors:
            distance = abs(event_position - sensor)
            time_delay = distance / self.wave_speed  # Час затримки у секундах

            for t in range(time_steps):
                if t >= time_delay:
                    if t in self.data_handler.data.index and f"Pressure_{sensor}m" in self.data_handler.data.columns:
                        self.data_handler.data.loc[t, f"Pressure_{sensor}m"] -= pressure_decrease_rate
                        if self.data_handler.data.loc[t, f"Pressure_{sensor}m"] < 0:
                            self.data_handler.data.loc[t, f"Pressure_{sensor}m"] = 0  # Мінімальний тиск

                        # Падіння витрати
                        self.data_handler.data.loc[t, f"FlowRate_{sensor}m"] *= 0.95

                        # Логування перевищення порогу дельт
                        delta = self.data_handler.data.loc[t, f"Pressure_{sensor}m"] - self.data_handler.data.loc[t - 1, f"Pressure_{sensor}m"] if t > 0 else 0
                        if abs(delta) > 0.04:
                            self.logger.log(f"Дельта тиску на сенсорі {sensor} м перевищила поріг: {delta:.2f} атм на часі {t}.")
