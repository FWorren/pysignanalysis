import time
import numpy as np
import matplotlib.pylab as plt
import pysignanalysis.emd as emddev
import pysignanalysis.eemd as eemddev
import pysignanalysis.visualization as plotter
import pysignanalysis.hht as hht
import ptsa.emd as emdlib


if __name__ == '__main__':
    max_modes = 5
    ensembles = 100
    ensembles_per_thread = 5
    n_siftings = 200
    end_time = 1
    sample_freq = 1000
    noise_std = 0.2
    a_0 = 20
    a_1 = 30
    a_2 = 50
    a_3 = 10
    omega_0 = 60.0 * 2.0 * np.pi
    omega_1 = 30.0 * 2.0 * np.pi
    omega_2 = 20.0 * 2.0 * np.pi
    omega_3 = 10.0 * 2.0 * np.pi
    time_ax = np.linspace(0, end_time, end_time * sample_freq)
    sine_wave = a_0 * np.sin(omega_0 * time_ax) + \
                a_1 * np.sin(omega_1 * time_ax) + \
                a_2 * np.sin(omega_2 * time_ax) + \
                a_3 * np.sin(omega_3 * time_ax)

    start = time.time()
    imfs = eemddev.eemd(sine_wave, sample_freq, noise_std, max_modes, ensembles, ensembles_per_thread)
    imfs_emd = emddev.emd(sine_wave, max_modes)
    print "Process time developed: ", time.time() - start
    start = time.time()
    #imfs_2 = emdlib.eemd(sine_wave, noise_std, ensembles, n_siftings)
    print "Process time lib: ", time.time() - start
    frequencies, amplitudes = hht.hht(sample_freq, imfs)
    plotter.plot_intrinsic_mode_functions(sample_freq, imfs, 'Developed EEMD', plt)
    plotter.plot_intrinsic_mode_functions(sample_freq, imfs_emd, 'Developed EMD', plt)
    #plotter.plot_intrinsic_mode_functions(sample_freq, imfs_2, 'Lib EMD', plt)
    # plotter.plot_time_frequency_series(sample_freq, frequencies, "Test", plt)
    # #plotter.plot_hilbert_spectra(time_ax, frequencies, amplitudes, "test", plt, sample_freq)
    plt.show()
