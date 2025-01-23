import numpy as np
import pandas as pd

class Pipeline:
    """
    Клас для моделювання трубопроводу та генерації даних потоку.
    """
    def __init__(self, length, diameter, sensors, pressure_norm, flow_rate_norm):
        self.length = length
        self.diameter = diameter
        self.sensors = sensors
        self.pressure_norm = pressure_norm
        self.flow_rate_norm = flow_rate_norm
        self.area = np.pi * (self.diameter ** 2) / 4
        self.data = None

    def generate_normal_flow(self, time_steps, noise_level):
        """
        Генерує дані для стабільного потоку через трубопровід.
        """
        data = {
            "Time": np.linspace(0, time_steps, time_steps),
        }
        for sensor in self.sensors:
            data[f"Pressure_{sensor}m"] = self.pressure_norm + np.random.uniform(
                -noise_level, noise_level, time_steps
            )
            data[f"FlowRate_{sensor}m"] = self.flow_rate_norm + np.random.uniform(
                -noise_level, noise_level, time_steps
            )
        self.data = pd.DataFrame(data)
