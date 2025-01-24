import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Завантаження даних
file_path = "Data/Pipeline_Event_Simulation.csv"
data = pd.read_csv(file_path)

# Підготовка даних
if "Anomaly" not in data.columns:
    raise ValueError("Стовпець 'Anomaly' відсутній у файлі даних. Перевірте генерацію даних.")

features = data.drop(columns=["Anomaly", "Time"], errors='ignore')
labels = data["Anomaly"]

# Розділення на тренувальну і тестову вибірки
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Ініціалізація та навчання моделі
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Прогнозування
y_pred = model.predict(X_test)

# Оцінка моделі
print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Візуалізація матриці плутанини
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Normal", "Anomaly"], yticklabels=["Normal", "Anomaly"])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Збереження моделі (якщо потрібно для подальшого використання)
import joblib
model_output_path = "Data/Anomaly_Detection_Model.pkl"
joblib.dump(model, model_output_path)
print(f"Модель збережено у файл: {model_output_path}")