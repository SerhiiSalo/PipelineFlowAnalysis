import matplotlib.pyplot as plt




class Visualization:
    """
    Клас для візуалізації даних трубопроводу.
    """
    def __init__(self, data_handler):
        self.data_handler = data_handler

    def plot_data(self, sensors):
        """
        Побудова графіків для перевірки даних трубопроводу.
        """
        if self.data_handler.data is None:
            print("Дані ще не згенеровані.")
            return

        plt.figure(figsize=(14, 12))

        plt.subplot(3, 1, 1)
        for sensor in sensors:
            plt.plot(self.data_handler.data["Time"], self.data_handler.data[f"Pressure_{sensor}m"], label=f"Тиск на {sensor} м")
        plt.title("Тиск у часі")
        plt.xlabel("Час")
        plt.ylabel("Тиск (атм)")
        plt.legend()
        plt.grid()

        plt.subplot(3, 1, 2)
        for sensor in sensors:
            plt.plot(self.data_handler.data["Time"], self.data_handler.data[f"FlowRate_{sensor}m"], label=f"Витрата на {sensor} м")
        plt.title("Об'ємна витрата у часі")
        plt.xlabel("Час")
        plt.ylabel("Витрата (м³/с)")
        plt.legend()
        plt.grid()

        plt.subplot(3, 1, 3)
        for sensor in sensors:
            deltas = self.data_handler.data[f"Pressure_{sensor}m"].diff().fillna(0)
            plt.plot(self.data_handler.data["Time"], deltas, label=f"Дельта тиску на {sensor} м")
            plt.axhline(0.02, color='red', linestyle='--', label="Поріг аномалій")
            plt.axhline(-0.02, color='red', linestyle='--')
        plt.title("Дельта тиску у часі")
        plt.xlabel("Час")
        plt.ylabel("Дельта тиску (атм)")
        plt.legend()
        plt.grid()

        plt.tight_layout()
        plt.show(block=True)