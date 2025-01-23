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

        plt.figure(figsize=(14, 8))
        for sensor in sensors:
            plt.subplot(3, 1, 1)
            plt.plot(self.data_handler.data["Time"], self.data_handler.data[f"Pressure_{sensor}m"], label=f"Тиск на {sensor} м")
            plt.title("Тиск у часі")
            plt.xlabel("Час")
            plt.ylabel("Тиск (атм)")
            plt.legend()
            plt.grid()

            plt.subplot(3, 1, 2)
            plt.plot(self.data_handler.data["Time"], self.data_handler.data[f"FlowRate_{sensor}m"], label=f"Витрата на {sensor} м")
            plt.title("Об'ємна витрата у часі")
            plt.xlabel("Час")
            plt.ylabel("Витрата (м³/с)")
            plt.legend()
            plt.grid()

            # Розрахунок дельт
            deltas = self.data_handler.data[f"Pressure_{sensor}m"].diff().fillna(0)
            threshold = 0.04
            plt.subplot(3, 1, 3)
            plt.plot(self.data_handler.data["Time"], deltas, label=f"Дельта тиску на {sensor} м")
            plt.axhline(y=threshold, color='r', linestyle='--', label="Поріг аномалій")
            plt.axhline(y=-threshold, color='r', linestyle='--')
            anomalies = deltas[abs(deltas) > threshold]
            plt.scatter(self.data_handler.data["Time"].iloc[anomalies.index], anomalies, color='orange', label="Аномалії")
            plt.title("Дельта тиску у часі")
            plt.xlabel("Час")
            plt.ylabel("Дельта тиску (атм)")
            plt.legend()
            plt.grid()

        plt.tight_layout()
        plt.show()
