from DataGenerator import SimulationDataGenerator
from check_anomalies import AnomalyChecker
from Visualization import Visualization
from DataHandler import DataHandler

class Coordinator:
    """
    Клас для координації імітації реальної роботи системи.
    """
    def __init__(self, model_path="Data/Anomaly_Detection_Model.pkl"):
        """
        Ініціалізує Coordinator із заданим шляхом до моделі.

        Parameters:
        - model_path (str): Шлях до файлу моделі.
        """
        self.model_path = model_path

    def simulate_single_iteration(self, sensors):
        """
        Симулює одиничну ітерацію отримання даних із сенсорів, виводить графік і перевіряє на аномалії.

        Parameters:
        - sensors (list): Позиції сенсорів.
        """
        # Генерація одиничного набору даних
        generator = SimulationDataGenerator()
        generator.generate_data(time_steps=1, sensors=sensors, include_failure=False, include_theft=False)
        single_data = generator.data

        # Зберігаємо одиничний набір даних у тимчасовий файл
        temp_file = "Data/Single_Iteration.csv"
        single_data.to_csv(temp_file, index=False)
        print(f"Дані для одиничної ітерації збережено у файл: {temp_file}")

        print("Дані для одиничної ітерації:")
        print(single_data)
        single_data.to_csv("debug_single_iteration.csv", index=False)

        # Створення та завантаження даних у DataHandler
        data_handler = DataHandler()
        data_handler.load_data(temp_file)

        # Візуалізація даних
        viz = Visualization(data_handler)
        viz.plot_single_iteration(sensors)

        # Перевірка на аномалії
        checker = AnomalyChecker(model_path=self.model_path)
        checker.check_data(temp_file)


if __name__ == "__main__":
    # Приклад використання Coordinator
    coordinator = Coordinator()

    # Симуляція одиничної ітерації
    sensors = [0, 150_000, 250_000, 300_000]
    coordinator.simulate_single_iteration(sensors=sensors)
