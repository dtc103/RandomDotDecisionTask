import numpy as np
import pandas as pd

def pos_to_angle(x, y):
    angle = np.arctan2(y, x) - np.pi 

    if angle < 0:
        angle += 2*np.pi

    return angle

def save_data(data, subject_name, header):
    data = pd.DataFrame(data)

    data.to_csv(f"C:/Users/jan_k/OneDrive - bwedu/Banburismus_presentation/RandomDotDecisionTask/data/{subject_name}.csv", index=False, header=header)