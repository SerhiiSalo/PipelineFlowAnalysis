from DataGenerator import SimulationDataGenerator
from check_anomalies import AnomalyChecker

class Coordinator:
    """
    Клас для координації основних дій у проєкті: генерація даних та перевірка на аномалії.
    """
    def __init__(self, data_path="Data/Pipeline_Event_Simulation.csv", model_path="Data/Anomaly_Detection_Model.pkl"):
        """
        Ініціалізує Coordinator із заданими шляхами до файлів.

        Parameters:
        - data_path (str): Шлях до файлу з даними.
        - model_path (str): Шлях до файлу моделі.
        """
        self.data_path = data_path
        self.model_path = model_path

    def generate_data(self, include_failure=False, include_theft=False, time_steps=100, sensors=None):
        """
        Генерує дані трубопроводу з можливістю додавання аварій та крадіжок.

        Parameters:
        - include_failure (bool): Чи включати аварії.
        - include_theft (bool): Чи включати крадіжки.
        - time_steps (int): Кількість часових кроків.
        - sensors (list): Позиції сенсорів.
        """
        if sensors is None:
            sensors = [0, 150_000, 250_000, 300_000]

        generator = SimulationDataGenerator()
        generator.generate_data(time_steps=time_steps, sensors=sensors, include_failure=include_failure, include_theft=include_theft)
        generator.save_data(self.data_path)
        print(f"Дані збережено у файл {self.data_path}")


    def check_data(self):
        """
        Перевіряє дані на наявність аномалій за допомогою збереженої моделі.
        """
        checker = AnomalyChecker(model_path=self.model_path)
        checker.check_data(data_path=self.data_path)

if __name__ == "__main__":
    # Приклад використання Coordinator
    coordinator = Coordinator()

    # Генерація даних із аваріями та крадіжками
    print("Генеруємо дані...")
    coordinator.generate_data(time_steps=200, sensors=[0, 150_000, 250_000, 300_000], include_failure=True, include_theft=True)

    # Перевірка даних
    print("Перевіряємо дані...")
    coordinator.check_data()
