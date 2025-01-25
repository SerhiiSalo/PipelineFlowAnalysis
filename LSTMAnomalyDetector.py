import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import pandas as pd

from TrainingDataProcessor import TrainingDataProcessor

class LSTMDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

class LSTMAnomalyDetector(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTMAnomalyDetector, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return torch.sigmoid(out)

def train_model(model, train_loader, val_loader, num_epochs, criterion, optimizer):
    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0

        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.float(), y_batch.float()
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch.unsqueeze(1))
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        train_loss /= len(train_loader)

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch, y_batch = X_batch.float(), y_batch.float()
                outputs = model(X_batch)
                loss = criterion(outputs, y_batch.unsqueeze(1))
                val_loss += loss.item()

        val_loss /= len(val_loader)
        print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {train_loss:.4f}, Validation Loss: {val_loss:.4f}")

    def simulate_real_work(model, data_file, log_file="simulation_log.txt", threshold=0.5):
        print("Починається симуляція реальної роботи...")

        if not os.path.exists(data_file):
            print(f"Файл {data_file} не знайдено.")
            return

        with open(log_file, "w") as log:
            log.write("Time,Prediction,Actual,Anomaly_Detected\n")
            
            data = pd.read_csv(data_file)
            for index, row in data.iterrows():
                # Видаляємо колонку "label" перед формуванням вхідних даних
                input_data = torch.tensor(row[:-1].values).float().unsqueeze(0).unsqueeze(0)  # Формуємо вектор для моделі
                prediction = model(input_data).item()
                actual = row["label"]

                anomaly_detected = "Yes" if prediction >= threshold else "No"
                log.write(f"{row['Time']},{prediction:.4f},{actual},{anomaly_detected}\n")

                if anomaly_detected == "Yes":
                    print(f"Аномалія виявлена на {row['Time']} секунді! Ймовірність: {prediction:.4f}")


if __name__ == "__main__":
    processor = TrainingDataProcessor()
    data_file = "Processed_Data/Merged_Training_Data.csv"

    print("Завантаження та підготовка даних...")
    all_data = processor.load_and_label_data(data_file)
    X_train, y_train, X_val, y_val, X_test, y_test = processor.prepare_data_for_lstm(all_data)

    train_dataset = LSTMDataset(torch.tensor(X_train), torch.tensor(y_train))
    val_dataset = LSTMDataset(torch.tensor(X_val), torch.tensor(y_val))
    test_dataset = LSTMDataset(torch.tensor(X_test), torch.tensor(y_test))

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

    input_size = X_train.shape[2]
    hidden_size = 64
    num_layers = 2
    num_epochs = 20

    model = LSTMAnomalyDetector(input_size, hidden_size, num_layers)
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    print("Починається навчання моделі...")
    train_model(model, train_loader, val_loader, num_epochs, criterion, optimizer)
    print("Навчання завершено.")

    # Зберігаємо модель
    model_path = "lstm_anomaly_detector.pth"
    torch.save(model.state_dict(), model_path)
    print(f"Модель збережено у файл: {model_path}")

    # Симуляція реальної роботи
    #simulate_real_work(model, data_file)
