import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

class TrainingDataProcessor:
    def __init__(self):
        pass

    def load_and_label_data(self, file_path):
        """
        Завантажує дані з CSV файлу. Якщо файл уже містить колонку 'label',
        пропускає додавання міток.
        """
        data = pd.read_csv(file_path)
        if "label" not in data.columns:
            if "Training_N_" in file_path:
                data["label"] = 0
            elif "Training_A_" in file_path:
                data["label"] = 1
            else:
                raise ValueError("Неможливо визначити мітку для даних: перевірте шлях до файлу.")
        return data

    def merge_and_label_from_directories(self, base_dir):
        """
        Об'єднує дані з усіх підкаталогів у базовому каталозі, додаючи мітки.
        """
        all_data = []
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    try:
                        labeled_data = self.load_and_label_data(file_path)
                        all_data.append(labeled_data)
                    except ValueError as e:
                        print(f"Пропущено файл {file_path}: {e}")

        if not all_data:
            raise ValueError("Не знайдено жодного валідного файлу для об'єднання.")

        merged_data = pd.concat(all_data, ignore_index=True)
        return merged_data

    def save_merged_data(self, merged_data, output_file):
        """
        Зберігає об'єднані дані в CSV файл.
        """
        merged_data.to_csv(output_file, index=False)
        print(f"Дані успішно збережено у файл: {output_file}")

    def prepare_data_for_lstm(self, data, sequence_length=50):
        """
        Підготовка даних для LSTM моделі.
        Перетворює таблицю даних у послідовності для навчання.
        """
        feature_columns = [col for col in data.columns if col not in ["Time", "label"]]
        X = []
        y = []
        
        data_values = data[feature_columns].values
        labels = data["label"].values

        for i in range(len(data) - sequence_length):
            X.append(data_values[i:i+sequence_length])
            y.append(labels[i+sequence_length])

        X = np.array(X)
        y = np.array(y)

        # Розділення на train, validation, test
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

        return X_train, y_train, X_val, y_val, X_test, y_test

if __name__ == "__main__":
    processor = TrainingDataProcessor()
    base_directory = "Data"
    output_file = "Processed_Data/Merged_Training_Data.csv"

    print("Починається об'єднання даних...")
    merged_data = processor.merge_and_label_from_directories(base_directory)
    print("Дані успішно об'єднано.")

    print("Зберігання об'єднаних даних...")
    processor.save_merged_data(merged_data, output_file)
    print("Процес завершено.")
