import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class TrainingDataProcessor:
    def load_and_label_data(self, file_path):
        """
        Завантажує дані з CSV-файлу і додає мітки.
        """
        data = pd.read_csv(file_path)
        # Перевіряємо наявність колонки 'label'
        if 'label' not in data.columns:
            raise ValueError("У файлі відсутня колонка 'label'.")
        return data

    def prepare_data_for_lstm(self, data, test_size=0.2, val_size=0.2, sequence_length=10):
        """
        Підготовлює дані для моделі LSTM: нормалізує, створює послідовності та розділяє на набори.
        """
        # Нормалізація даних
        scaler = MinMaxScaler()
        feature_columns = [col for col in data.columns if col != 'label']
        data[feature_columns] = scaler.fit_transform(data[feature_columns])

        # Створення послідовностей
        sequences = []
        labels = []
        for i in range(len(data) - sequence_length):
            seq = data.iloc[i:i+sequence_length][feature_columns].values
            label = data.iloc[i+sequence_length-1]['label']
            sequences.append(seq)
            labels.append(label)

        X = np.array(sequences)
        y = np.array(labels)

        # Розділення на тренувальні, валідаційні та тестові набори
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=test_size, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

        return X_train, y_train, X_val, y_val, X_test, y_test
