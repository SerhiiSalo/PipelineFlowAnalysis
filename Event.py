
class Event:
    """
    Базовий клас для подій на трубопроводі (крадіжка, аварія тощо).
    """
    def __init__(self, data_handler):
        self.data_handler = data_handler

    def apply_event(self):
        """
        Застосовує подію до даних.
        """
        raise NotImplementedError("Метод apply_event() має бути реалізований у дочірньому класі.")