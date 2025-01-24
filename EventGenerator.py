import random

class EventGenerator:
    """
    Клас для генерації позицій подій (наприклад, аварій) на трубопроводі.
    """

    def __init__(self, pipeline_length, sensors, min_distance_from_sensors, logger):
        """
        Ініціалізує об'єкт EventGenerator з необхідними параметрами.

        Parameters:
        - pipeline_length (int): Довжина трубопроводу в метрах.
        - sensors (list): Список позицій сенсорів уздовж трубопроводу.
        - min_distance_from_sensors (int): Мінімальна відстань від сенсора до події.
        - logger (Logger): Об'єкт логера для запису подій.
        """
        self.pipeline_length = pipeline_length  # Довжина трубопроводу
        self.sensors = sensors  # Позиції сенсорів
        self.min_distance_from_sensors = min_distance_from_sensors  # Мінімальна відстань до сенсора
        self.logger = logger  # Логер для запису подій

    def generate_event_position(self):
        """
        Генерує випадкову позицію для події, яка знаходиться на певній відстані від сенсорів.

        Returns:
        int: Згенерована позиція події в межах трубопроводу.
        """
        while True:
            position = random.randint(0, self.pipeline_length)  # Генеруємо випадкову позицію
            valid = True  # Припускаємо, що позиція є валідною

            # Перевіряємо, чи знаходиться подія на допустимій відстані від усіх сенсорів
            for sensor in self.sensors:
                if abs(position - sensor) < self.min_distance_from_sensors:
                    valid = False  # Позиція занадто близько до сенсора
                    break

            if valid:  # Якщо позиція валідна, виходимо з циклу
                self.logger.log(f"Згенеровано подію на позиції: {position} м", level="INFO")
                return position
            else:
                self.logger.log("Позиція події не відповідає умовам. Спроба знову.", level="WARNING")
