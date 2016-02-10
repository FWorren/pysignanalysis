import numpy as np


def normalize_data(data):
    max_data = np.max(data)
    min_data = np.min(data)
    diff = max_data - min_data
    data_norm = np.zeros(len(data))
    for i in range(len(data)):
        data_norm[i] = (data[i] - min_data) / diff
    return data_norm
