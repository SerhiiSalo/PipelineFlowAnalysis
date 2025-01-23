import random


class EventGenerator:
    """
    Клас для генерації місця аварії або крадіжки.
    """
    def __init__(self, pipeline_length, sensors, min_distance_from_sensors, logger):
        self.pipeline_length = pipeline_length
        self.sensors = sensors
        self.min_distance_from_sensors = min_distance_from_sensors
        self.logger = logger

    def generate_event_position(self):
        """
        Генерує місце аварії/крадіжки, яке відповідає умовам.
        """
        while True:
            event_position = random.randint(0, self.pipeline_length)
            # Перевірка відстані від сенсорів
            if all(abs(event_position - sensor) >= self.min_distance_from_sensors for sensor in self.sensors):
                return event_position
