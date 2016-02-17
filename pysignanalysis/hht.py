import numpy as np
import scipy.signal as signal


def hilbert_transform(sample_frequency, imfs):
    amplitudes = np.zeros(imfs.shape, np.float32)
    phase = np.zeros(imfs.shape, np.float32)
    frequencies = np.zeros(imfs.shape, np.float32)

    for i in range(len(imfs)):
        h = signal.hilbert(imfs[i])
        amplitudes[i, :] = np.abs(h)
        phase[i, :] = np.angle(h)
        frequencies[i, :] = np.r_[
            0.0,
            0.5*(np.angle(-h[2:]*np.conj(h[0:-2]))+np.pi)/(2.0*np.pi) * np.float32(sample_frequency),
            0.0
        ]
        max_freq = 400
        for k in range(len(frequencies[i])):
            if frequencies[i, k] > max_freq:
                if k > 0:
                    frequencies[i, k] = frequencies[i, k-1]
                else:
                    frequencies[i, k] = max_freq

    return frequencies, amplitudes
