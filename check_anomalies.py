import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

class AnomalyChecker:
    """
    Клас для перевірки наявності аномалій у збережених даних.
    """
    def __init__(self, model_path):
        """
        Ініціалізує об'єкт AnomalyChecker.

        Parameters:
        - model_path (str): Шлях до збереженої моделі.
        """
        self.model = joblib.load(model_path)  # Завантаження моделі
        self.expected_features = self.model.feature_names_in_  # Зберігаємо ознаки, використані під час навчання

    def check_data(self, data_path):
        """
        Перевіряє дані на наявність аномалій.

        Parameters:
        - data_path (str): Шлях до файлу з даними.
        """
        # Завантаження даних
        data = pd.read_csv(data_path)

        if "Anomaly" not in data.columns:
            raise ValueError("Стовпець 'Anomaly' відсутній у даних. Перевірте структуру файлу.")

        features = data.drop(columns=["Anomaly", "Time"], errors='ignore')

        # Перевірка відповідності набору ознак
        for missing_feature in set(self.expected_features) - set(features.columns):
            features[missing_feature] = 0  # Додаємо відсутні ознаки з нульовими значеннями

        features = features[self.expected_features]  # Упорядковуємо стовпці відповідно до моделі

        true_labels = data["Anomaly"]

        # Прогнозування
        predictions = self.model.predict(features)

        # Оцінка
        print("Classification Report:")
        print(classification_report(true_labels, predictions))

        print("Confusion Matrix:")
        cm = confusion_matrix(true_labels, predictions)
        print(cm)

        # Візуалізація матриці плутанини
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Normal", "Anomaly"], yticklabels=["Normal", "Anomaly"])
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.show()

if __name__ == "__main__":
    # Ініціалізація об'єкта
    model_path = "Data/Anomaly_Detection_Model.pkl"
    data_path = "Data/Pipeline_Event_Simulation.csv"

    checker = AnomalyChecker(model_path=model_path)

    # Перевірка даних
    checker.check_data(data_path=data_path)
