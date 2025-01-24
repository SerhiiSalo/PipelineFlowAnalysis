import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Завантаження даних
file_path = "Data/Pipeline_Event_Simulation.csv"  # Шлях до файлу з даними

data = pd.read_csv(file_path)  # Читання даних із CSV-файлу

# Перевірка наявності стовпця 'Anomaly'
if "Anomaly" not in data.columns:
    raise ValueError("Стовпець 'Anomaly' відсутній у файлі даних. Перевірте генерацію даних.")

# Розділення даних на особливості (features) і мітки (labels)
features = data.drop(columns=["Anomaly", "Time"], errors='ignore')  # Видаляємо мітки та час
labels = data["Anomaly"]  # Використовуємо стовпець 'Anomaly' як мітки

# Розділення на тренувальну і тестову вибірки
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)  # 80% для навчання, 20% для тесту

# Ініціалізація та навчання моделі
model = RandomForestClassifier(n_estimators=100, random_state=42)  # Створення моделі Random Forest
model.fit(X_train, y_train)  # Навчання моделі на тренувальних даних

# Прогнозування
y_pred = model.predict(X_test)  # Прогноз для тестових даних

# Оцінка моделі
print("Classification Report:")
print(classification_report(y_test, y_pred))  # Вивід метрик точності

print("Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)  # Матриця плутанини
print(cm)

# Візуалізація матриці плутанини
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Normal", "Anomaly"], yticklabels=["Normal", "Anomaly"])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Збереження моделі (для подальшого використання)
import joblib
model_output_path = "Data/Anomaly_Detection_Model.pkl"  # Шлях для збереження моделі
joblib.dump(model, model_output_path)  # Збереження моделі у файл
print(f"Модель збережено у файл: {model_output_path}")
