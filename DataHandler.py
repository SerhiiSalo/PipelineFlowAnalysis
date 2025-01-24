import pandas as pd
import os
import time

class DataHandler:
    """
    Клас для роботи з даними: завантаження і збереження у форматі CSV.
    """

    def __init__(self):
        """
        Ініціалізує об'єкт DataHandler з атрибутом для зберігання даних.
        """
        self.data = None  # Зберігає основні дані, завантажені або згенеровані

    def save_data(self, file_name):
        """
        Зберігає дані у файл CSV.

        Parameters:
        file_name (str): Ім'я файлу для збереження даних.
        """
        if self.data is not None:  # Перевіряємо, чи є дані для збереження
            self.data.to_csv(file_name, index=False)  # Зберігаємо у форматі CSV без індексів
            print(f"Дані успішно збережені у файл: {file_name}")
        else:
            print("Дані відсутні. Немає чого зберігати.")  # Повідомлення, якщо даних немає

    def load_data(self, file_name):
        """
        Завантажує дані з файлу CSV.

        Parameters:
        file_name (str): Ім'я файлу, з якого потрібно завантажити дані.
        """
        try:
            self.data = pd.read_csv(file_name)  # Завантаження даних у pandas DataFrame
            print(f"Дані успішно завантажені з файлу: {file_name}")
        except FileNotFoundError:
            print(f"Файл {file_name} не знайдено. Перевірте шлях до файлу.")  # Повідомлення про відсутність файлу
        except pd.errors.EmptyDataError:
            print(f"Файл {file_name} порожній. Завантаження неможливе.")  # Повідомлення про порожній файл
        except Exception as e:
            print(f"Сталася помилка при завантаженні даних: {e}")  # Вивід будь-яких інших помилок

    def prepare_environment(storage_mode, base_path="Data"):
        """
        Підготовка середовища для зберігання даних симуляції.
        """
        if storage_mode == "overwrite":
            if not os.path.exists(base_path):
                os.mkdir(base_path)
            else:
                for file in os.listdir(base_path):
                    os.remove(os.path.join(base_path, file))
        elif storage_mode == "separate":
            output_folder = f"{base_path}/Training_{time.strftime('%Y%m%d_%H%M%S')}"
            if not os.path.exists(output_folder):  # Перевірка існування папки
                os.mkdir(output_folder)
            return output_folder
        return base_path