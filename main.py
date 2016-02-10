import time
import numpy as np
import matplotlib.pylab as plt
import pysignanalysis.emd as emddev
import pysignanalysis.visualization as plotter
import pysignanalysis.hht as hht

if __name__ == '__main__':
    max_modes = 5
    end_time = 1
    sample_freq = 500
    a_0 = 40
    a_1 = 30
    a_2 = 20
    a_3 = 10
    omega_0 = 50.0 * 2.0 * np.pi
    omega_1 = 30.0 * 2.0 * np.pi
    omega_2 = 20.0 * 2.0 * np.pi
    omega_3 = 10.0 * 2.0 * np.pi
    time_ax = np.linspace(0, end_time, end_time * sample_freq)
    sine_wave = a_0 * np.sin(omega_0 * time_ax) + \
                a_1 * np.sin(omega_1 * time_ax) + \
                a_2 * np.sin(omega_2 * time_ax) + \
                a_3 * np.sin(omega_3 * time_ax)

    start = time.time()
    imfs = emddev.emd(sine_wave, max_modes)
    frequencies, amplitudes = hht.hht(sample_freq, imfs)
    print "Process time developed: %d", time.time() - start
    plotter.plot_intrinsic_mode_functions(sample_freq, imfs, 'Developed EMD', plt)
    plotter.plot_time_frequency_series(sample_freq, frequencies, "Test", plt)
    #plotter.plot_hilbert_spectra(time_ax, frequencies, amplitudes, "test", plt, sample_freq)
    plt.show()
