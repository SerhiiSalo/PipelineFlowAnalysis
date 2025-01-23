import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Константи для симуляції
D = 1.02  # Діаметр труби у метрах
rho = 850  # Густина нафти в кг/м³
A = np.pi * (D ** 2) / 4  # Площа перерізу у м²
L = 300_000  # Довжина труби у метрах

# Параметри симуляції
PRESSURE_NORM = 34.0  # Стабільний тиск у нормальних умовах (атм)
FLOW_RATE_NORM = 3.5  # Стабільна об'ємна витрата у нормальних умовах (м³/с)
SENSORS = [0, 150_000, 250_000, 300_000]  # Розташування сенсорів у метрах
TIME_STEPS = 100  # Кількість часових точок
NOISE_LEVEL = 0.02  # Шум у даних (±2%)


# Функція для генерації стабільного потоку
def generate_normal_flow(time_steps, sensors):
    """
    Генерує дані для стабільного потоку через трубу.
    """
    data = {
        "Time": np.linspace(0, time_steps, time_steps),
    }
    for sensor in sensors:
        # Додавання стабільного тиску з невеликим шумом
        data[f"Pressure_{sensor}m"] = PRESSURE_NORM + np.random.uniform(
            -NOISE_LEVEL/2, NOISE_LEVEL/2, time_steps
        )

        # Додавання стабільної витрати з шумом
        data[f"FlowRate_{sensor}m"] = FLOW_RATE_NORM + np.random.uniform(
            -NOISE_LEVEL/2, NOISE_LEVEL/2, time_steps
        )
    return pd.DataFrame(data)

# Функція для додавання аномальних подій
def add_anomalies(data, sensors):
    """
    Додає аномальні події до даних: падіння тиску, зростання витрати, пропуски.
    """
    # Падіння тиску на сенсорі 150 км
    anomaly_index = TIME_STEPS // 3
    data.loc[anomaly_index, f"Pressure_{sensors[1]}m"] -= 5  # Різке падіння на 5 атм

    # Зростання витрати на сенсорі 250 км
    data.loc[anomaly_index + 10, f"FlowRate_{sensors[2]}m"] *= 1.5  # Збільшення на 50%

    # Пропуски даних для сенсора 300 км
    missing_start = TIME_STEPS // 2
    missing_end = missing_start + 5
    data.loc[missing_start:missing_end, f"Pressure_{sensors[3]}m"] = None
    data.loc[missing_start:missing_end, f"FlowRate_{sensors[3]}m"] = None
    
    # Інтерполяція пропусків
    data.interpolate(inplace=True)
    return data

# Генерація нормального потоку
normal_data = generate_normal_flow(TIME_STEPS, SENSORS)

# Додавання аномалій
data_with_anomalies = add_anomalies(normal_data, SENSORS)


# Збереження даних у файл
output_path = "Pipeline_Simulation_Data.csv"
data_with_anomalies.to_csv(output_path, index=False)

# Графічна візуалізація
def plot_simulation_data(data, sensors):
    """
    Побудова графіків для перевірки нормального потоку та аномалій.
    """
    plt.figure(figsize=(14, 8))

    for sensor in sensors:
        # Графік тиску
        plt.subplot(2, 1, 1)
        plt.plot(data["Time"], data[f"Pressure_{sensor}m"], label=f"Тиск на {sensor} м")
        plt.title("Тиск у часі")
        plt.xlabel("Час")
        plt.ylabel("Тиск (атм)")
        plt.legend()
        plt.grid()

        # Графік об'ємної витрати
        plt.subplot(2, 1, 2)
        plt.plot(data["Time"], data[f"FlowRate_{sensor}m"], label=f"Витрата на {sensor} м")
        plt.title("Об'ємна витрата у часі")
        plt.xlabel("Час")
        plt.ylabel("Витрата (м³/с)")
        plt.legend()
        plt.grid()

    plt.tight_layout()
    plt.show()


# Побудова графіків
plot_simulation_data(data_with_anomalies, SENSORS)

print(f"Дані симуляції збережено у файл: {output_path}")
