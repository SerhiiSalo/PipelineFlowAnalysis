import random
from Event import Event

class TheftEvent(Event):
    """
    Клас для моделювання події крадіжки на трубопроводі.
    """
    def __init__(self, data_handler):
        super().__init__(data_handler)

    def apply_event(self):
        """
        Додає подію крадіжки до даних.

        Варіанти:
        1. Одномоментний сплеск і падіння.
        2. Сплеск із затримкою перед падінням.
        3. Рандомний порядок сплеску і падіння.
        """
        affected_sensor = random.choice(self.data_handler.data.columns[1::2])
        event_type = random.choice([1, 2, 3])
        event_start = random.randint(10, len(self.data_handler.data) - 10)

        if event_type == 1:
            self.data_handler.data.loc[event_start, affected_sensor] += 5
            self.data_handler.data.loc[event_start + 1, affected_sensor] -= 5

        elif event_type == 2:
            delay = random.randint(1, 5)
            self.data_handler.data.loc[event_start, affected_sensor] += 5
            self.data_handler.data.loc[event_start + delay, affected_sensor] -= 5

        elif event_type == 3:
            first_event = random.choice(["spike", "drop"])
            if first_event == "spike":
                self.data_handler.data.loc[event_start, affected_sensor] += 5
                self.data_handler.data.loc[event_start + 1, affected_sensor] -= 5
            else:
                self.data_handler.data.loc[event_start, affected_sensor] -= 5
                self.data_handler.data.loc[event_start + 1, affected_sensor] += 5

