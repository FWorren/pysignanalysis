import time
import numpy as np
import matplotlib.pylab as plt
import pysignanalysis.emd as emddev
import pysignanalysis.eemd as eemddev
import pysignanalysis.visualization as plotter
import pysignanalysis.hht as hht
import pysignanalysis.utils as utils


if __name__ == '__main__':
    max_modes = 6
    ensembles = 100
    ensembles_per_process = 5
    max_siftings = 200
    end_time = 1
    sample_freq = 500
    noise_std = 0.01

    a_0 = 5000
    a_1 = 2000
    a_2 = 1000
    a_3 = 500
    omega_0 = 50.0 * 2.0 * np.pi
    omega_1 = 25.0 * 2.0 * np.pi
    omega_2 = 10.0 * 2.0 * np.pi
    omega_3 = 5.0 * 2.0 * np.pi
    time_ax = np.linspace(0, end_time, end_time * sample_freq)
    sine_wave = a_0 * np.sin(omega_0 * time_ax) + \
                a_1 * np.sin(omega_1 * time_ax) + \
                a_2 * np.sin(omega_2 * time_ax) + \
                a_3 * np.sin(omega_3 * time_ax)

    data_length = len(sine_wave)
    # sine_wave = utils.normalize_data(sine_wave)

    # start = time.time()
    # imfs_eemd = eemddev.eemd(sine_wave, noise_std, max_modes, max_siftings, ensembles, ensembles_per_process)
    # print "Process time EEMD: ", time.time() - start

    start = time.time()
    imfs_emd = emddev.emd(sine_wave, max_modes, max_siftings)
    print "Process time EMD: ", time.time() - start

    # start = time.time()
    # imfs = eemddev.eemd_without_threading(sine_wave, sample_freq, noise_std, max_modes, max_siftings, ensembles)
    # print "Process time developed: ", time.time() - start

    # noise = np.random.randn(len(sine_wave))*noise_std
    # data = np.add(sine_wave, noise)
    # plotter.plot_single_channel(sample_freq, data, plt, "Test")

    # plotter.plot_intrinsic_mode_functions(sample_freq, imfs_eemd, 'Developed EEMD', plt)
    #
    # plotter.plot_intrinsic_mode_functions(sample_freq, imfs_emd, 'Developed EMD', plt)

    # frequencies_eemd, amplitudes_eemd = hht.hht(sample_freq, imfs_eemd)

    frequencies_emd, amplitudes_emd = hht.hht(sample_freq, imfs_emd)

    # plotter.plot_intrinsic_mode_functions_with_time_frequency_series(sample_freq, imfs_eemd, frequencies_eemd, 'EEMD', plt)

    plotter.plot_intrinsic_mode_functions_with_time_frequency_series(sample_freq, imfs_emd, frequencies_emd, 'EMD', plt)

    # plotter.plot_intrinsic_mode_functions(sample_freq, imfs_2, 'Lib EMD', plt)

    # plotter.plot_time_frequency_series(sample_freq, frequencies, "Test", plt)

    # plotter.plot_hilbert_spectra(time_ax, frequencies_emd, amplitudes_emd, "test", plt, sample_freq)
    plt.show(block=True)
