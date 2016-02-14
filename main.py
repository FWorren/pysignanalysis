import time
import numpy as np
import matplotlib.pylab as plt
import pysignanalysis.emd as emddev
import pysignanalysis.eemd as eemddev
import pysignanalysis.visualization as plotter
import pysignanalysis.hht as hht
# import ptsa.emd as emdlib


if __name__ == '__main__':
    max_modes = 6
    ensembles = 3
    ensembles_per_process = 1
    max_siftings = 200
    end_time = 1
    sample_freq = 1000
    noise_std = 0.2

    a_0 = 40
    a_1 = 30
    a_2 = 50
    a_3 = 10
    omega_0 = 50.0 * 2.0 * np.pi
    omega_1 = 30.0 * 2.0 * np.pi
    omega_2 = 60.0 * 2.0 * np.pi
    omega_3 = 10.0 * 2.0 * np.pi
    time_ax = np.linspace(0, end_time, end_time * sample_freq)
    sine_wave = a_0 * np.sin(omega_0 * time_ax) + \
                a_1 * np.sin(omega_1 * time_ax) + \
                a_2 * np.sin(omega_2 * time_ax) + \
                a_3 * np.sin(omega_3 * time_ax)

    start = time.time()
    data_length = len(sine_wave)

    imfs_eemd = eemddev.eemd(sine_wave, noise_std, max_modes, max_siftings, ensembles, ensembles_per_process)
    #imfs_eemd = eemddev.ensemble_process_test(sine_wave, max_modes, max_siftings, noise_std, ensembles)

    # noise = np.multiply(np.random.randn(data_length), noise_std)
    # noise_assisted_data = sine_wave + noise
    # imfs_emd = emddev.emd(noise_assisted_data, max_modes, max_siftings)
    # noise = np.multiply(np.random.randn(data_length), noise_std)
    # noise_assisted_data = sine_wave + noise
    # imfs_emd2 = emddev.emd(noise_assisted_data, max_modes, max_siftings)
    # noise = np.multiply(np.random.randn(data_length), noise_std)
    # noise_assisted_data = sine_wave + noise
    # imfs_emd3 = emddev.emd(noise_assisted_data, max_modes, max_siftings)
    # noise = np.multiply(np.random.randn(data_length), noise_std)
    # noise_assisted_data = sine_wave + noise
    # imfs_emd4 = emddev.emd(noise_assisted_data, max_modes, max_siftings)
    # imfs1 = np.add(imfs_emd, imfs_emd2)
    # imfs2 = np.add(imfs_emd3, imfs_emd4)
    # imfs = np.add(imfs1, imfs2)
    # imfs = np.multiply(imfs, 1/float(4))
    print "Process time developed: ", time.time() - start

    # start = time.time()
    # imfs_2 = emdlib.eemd(sine_wave, noise_std, ensembles, max_siftings)
    # print "Process time lib: ", time.time() - start

    # start = time.time()
    # imfs = eemddev.eemd_without_threading(sine_wave, sample_freq, noise_std, max_modes, max_siftings, ensembles)
    # print "Process time developed: ", time.time() - start

    # frequencies, amplitudes = hht.hht(sample_freq, imfs)

    # noise = np.random.randn(len(sine_wave))*noise_std
    # data = np.add(sine_wave, noise)
    # plotter.plot_single_channel(sample_freq, data, plt, "Test")

    plotter.plot_intrinsic_mode_functions(sample_freq, imfs_eemd, 'Developed EEMD', plt)

    # plotter.plot_intrinsic_mode_functions(sample_freq, imfs, 'Developed EEMD', plt)

    # plotter.plot_intrinsic_mode_functions(sample_freq, imfs_emd, 'Developed EMD', plt)

    # plotter.plot_intrinsic_mode_functions(sample_freq, imfs_2, 'Lib EMD', plt)

    # plotter.plot_time_frequency_series(sample_freq, frequencies, "Test", plt)

    # plotter.plot_hilbert_spectra(time_ax, frequencies, amplitudes, "test", plt, sample_freq)
    plt.show(block=True)
