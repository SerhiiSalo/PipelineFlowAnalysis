import pandas as pd

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