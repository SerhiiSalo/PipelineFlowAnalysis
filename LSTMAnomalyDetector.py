import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
from TrainingDataProcessor import TrainingDataProcessor

# Завантаження та підготовка даних
processor = TrainingDataProcessor()
all_data = processor.load_and_label_data("Processed_Data/Merged_Training_Data.csv")
X_train, y_train, X_val, y_val, X_test, y_test = processor.prepare_data_for_lstm(all_data)

class LSTMDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# Підготовка наборів даних
train_dataset = LSTMDataset(X_train, y_train)
val_dataset = LSTMDataset(X_val, y_val)
test_dataset = LSTMDataset(X_test, y_test)

# Створення завантажувачів даних
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

class LSTMAnomalyDetector(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(LSTMAnomalyDetector, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        out = self.fc(lstm_out[:, -1, :])  # Використовуємо останній часовий крок
        return out

# Ініціалізація моделі
input_dim = X_train.shape[2]
hidden_dim = 64
num_layers = 2
output_dim = 1

model = LSTMAnomalyDetector(input_dim, hidden_dim, num_layers, output_dim)

# Налаштування оптимізатора і функції втрат
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Тренування моделі
def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs=20):
    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs.squeeze(), y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * X_batch.size(0)

        train_loss /= len(train_loader.dataset)

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                outputs = model(X_batch)
                loss = criterion(outputs.squeeze(), y_batch)
                val_loss += loss.item() * X_batch.size(0)

        val_loss /= len(val_loader.dataset)

        print(f"Epoch {epoch + 1}/{num_epochs}, Train Loss: {train_loss:.4f}, Validation Loss: {val_loss:.4f}")

# Запуск тренування
train_model(model, train_loader, val_loader, criterion, optimizer)
