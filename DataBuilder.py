#--------------------
#    Клас застарів
#--------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Константи для розрахунків
D = 1.02  # Діаметр труби у метрах
rho = 850  # Густина нафти в кг/м³
A = np.pi * (D ** 2) / 4  # Площа перерізу у м²
ANOMALY_THRESHOLD_FLOW = 1.3  # Збільшений поріг для об'ємної витрати (30% перевищення середнього)
ANOMALY_THRESHOLD_PRESSURE = 7000  # Збільшений поріг для різниці тисків у Паскалях

# Завантаження даних
data = {
    "NumericValue_4006": [
        34.1730, 34.1370, 34.1920, 34.1300, 34.1510, 34.1670, 
        34.2150, 34.1620, 34.1770, 34.2360, 34.1160, 34.1110, 
        34.1690, None, 34.1660, 34.1670, 34.2150, 34.2360, 
        34.1620, None, 34.1770, 34.1690
    ],
    "TimeStamp": [
        "2023-11-23 14:02:00.840", "2023-11-23 13:02:01.357", 
        "2023-11-23 12:02:01.133", "2023-11-23 11:02:01.297", 
        "2023-11-23 10:02:00.833", "2023-11-23 09:10:01.107",
        "2023-11-23 09:10:01.107", "2023-11-23 09:10:01.090",
        "2023-11-23 09:10:01.090", "2023-11-23 09:10:01.090",
        "2023-11-23 09:10:01.073", "2023-11-23 09:10:01.073",
        "2023-11-23 09:10:01.073", "2023-11-23 09:10:01.060",
        "2023-11-23 09:10:01.060", "2023-11-23 09:02:07.107",
        "2023-11-23 08:02:06.347", "2023-11-23 07:02:06.097",
        "2023-11-23 06:02:05.140", "2023-11-23 06:02:05.127",
        "2023-11-23 05:01:04.880", "2023-11-23 04:02:04.470"
    ]
}

# Завантаження даних у DataFrame
df = pd.DataFrame(data)
df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])

# Інтерполяція для заповнення пропусків
df['NumericValue_4006'] = df['NumericValue_4006'].interpolate(method='linear')

# Розрахунок різниці тиску між послідовними вимірюваннями
df['PressureDrop'] = df['NumericValue_4006'].diff().fillna(0) * 101325  # З атмосфер у Па

# Розрахунок швидкості потоку та об'ємної витрати
df['Velocity'] = np.sqrt((2 * np.abs(df['PressureDrop'])) / rho)  # м/с
df['FlowRate'] = A * df['Velocity']  # м³/с

# Метод для визначення аномалій
def detect_anomalies(df):
    """
    Визначення аномалій за пороговими значеннями для тиску та об'ємної витрати.
    """
    mean_flow = df['FlowRate'].mean()  # Середнє значення об'ємної витрати
    
    # Умови для аномалій
    df['Anomaly'] = (
        (np.abs(df['PressureDrop']) > ANOMALY_THRESHOLD_PRESSURE) |  # Падіння тиску
        (df['FlowRate'] > mean_flow * ANOMALY_THRESHOLD_FLOW)  # Перевищення об'ємної витрати
    ).astype(int)  # 1 - аномалія, 0 - норма

    df['MeanFlow'] = mean_flow  # Збереження середнього значення об'ємної витрати для візуалізації

# Симуляція аварійних сценаріїв
def simulate_anomalies(df):
    """
    Додає в дані сценарії аварій для тестування алгоритму.

    Сценарії:
    1. Різке падіння тиску на певному сенсорі (зміна значення тиску).
    2. Збільшення об'ємної витрати, що імітує витік.
    3. Пропуски даних з подальшою інтерполяцією.
    """
    # Різке падіння тиску на певному сенсорі
    df.loc[5, 'NumericValue_4006'] -= 1.0  # Падіння на 1 атм
    
    # Збільшення витрати, що імітує витік
    df.loc[10, 'FlowRate'] *= 1.5  # Збільшення витрати на 50%

    # Пропуски в даних
    df.loc[15:17, 'NumericValue_4006'] = None  # Симуляція втрати даних
    df['NumericValue_4006'] = df['NumericValue_4006'].interpolate(method='linear')  # Повторна інтерполяція

# Виклик методу для симуляції аварій
simulate_anomalies(df)

# Повторний виклик для визначення аномалій
detect_anomalies(df)

# Графічна візуалізація
def plot_results(df):
    """
    Побудова графіків для аналізу даних та аномалій.
    """
    plt.figure(figsize=(14, 8))

    # Графік тиску
    plt.subplot(2, 1, 1)
    plt.plot(df['TimeStamp'], df['NumericValue_4006'], label='Тиск (атм)', color='blue')
    plt.scatter(df['TimeStamp'][df['Anomaly'] == 1], 
                df['NumericValue_4006'][df['Anomaly'] == 1], 
                color='red', label='Аномалії')
    plt.axhline(y=df['NumericValue_4006'].mean(), color='green', linestyle='--', label='Середній тиск')
    plt.title('Тиск у часі з виявленням аномалій')
    plt.xlabel('Час')
    plt.ylabel('Тиск (атм)')
    plt.legend()
    plt.grid()

    # Графік об'ємної витрати
    plt.subplot(2, 1, 2)
    plt.plot(df['TimeStamp'], df['FlowRate'], label="Об'ємна витрата (м³/с)", color='green')
    plt.scatter(df['TimeStamp'][df['Anomaly'] == 1], 
                df['FlowRate'][df['Anomaly'] == 1], 
                color='red', label='Аномалії')
    plt.axhline(y=df['MeanFlow'][0], color='blue', linestyle='--', label='Середня витрата')
    plt.axhline(y=df['MeanFlow'][0] * ANOMALY_THRESHOLD_FLOW, color='orange', linestyle='--', label='Поріг аномалії')
    plt.title("Об'ємна витрата у часі з виявленням аномалій")
    plt.xlabel('Час')
    plt.ylabel("Об'ємна витрата (м³/с)")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

# Побудова графіків
plot_results(df)

# Збереження таблиці з результатами в Excel
output_path = "Pressure_and_Flow_Rate_Analysis_with_Anomalies.xlsx"
df.to_excel(output_path, index=False)

print(f"Результати розрахунків та аномалій збережено у файл: {output_path}")
