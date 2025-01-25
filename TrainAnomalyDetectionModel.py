import torch
import pandas as pd
from LSTMAnomalyDetector import LSTMAnomalyDetector

class RealTimeAnomalyTester:
    def __init__(self, model_path, threshold=0.5):
        self.model = LSTMAnomalyDetector(input_size=8, hidden_size=64, num_layers=2)  # Змінено відповідно до структури моделі
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
        self.threshold = threshold

    def test_file(self, file_path):
        print(f"Починається тестування файлу: {file_path}")

        data = pd.read_csv(file_path)
        for index, row in data.iterrows():
            # Підготовка даних: беремо лише необхідні ознаки (без label)
            input_data = torch.tensor(row[:-1].values).float().unsqueeze(0).unsqueeze(0)

            # Прогноз моделі
            prediction = self.model(input_data).item()

            # Виведення результатів
            if prediction > self.threshold:
                print(f"Аномалія виявлена на рядку {index + 1}: {prediction:.4f}")
            else:
                print(f"Нормальний стан на рядку {index + 1}: {prediction:.4f}")

if __name__ == "__main__":
    model_path = "lstm_anomaly_detector.pth"
    test_file_path = "Data/Training_A_20250125_182449_29/Training_Data.csv"

    tester = RealTimeAnomalyTester(model_path, threshold=0.5)
    tester.test_file(test_file_path)
