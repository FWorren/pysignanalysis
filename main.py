import time
import numpy as np
import matplotlib.pylab as plt
import pysignanalysis.emd as emddev
import ptsa.emd as emdlib
import pysignanalysis.visualization as plotter

if __name__ == '__main__':
    max_modes = 5
    end_time = 1
    sample_freq = 2000
    a_0 = 100
    a_1 = 50
    a_2 = 10
    a_3 = 1
    omega_0 = 150.0 * 2.0 * np.pi
    omega_1 = 80.0 * 2.0 * np.pi
    omega_2 = 15.0 * 2.0 * np.pi
    omega_3 = 5.0 * 2.0 * np.pi
    time_ax = np.linspace(0, end_time, end_time * sample_freq)
    sine_wave = a_0 * np.sin(omega_0 * time_ax) + \
                a_1 * np.sin(omega_1 * time_ax + a_2 * np.sin(omega_2 * time_ax)) + \
                a_2 * np.sin(omega_2 * time_ax) + \
                a_3 * np.sin(omega_3 * time_ax)

    start = time.time()
    imfs = emddev.emd(sine_wave, max_modes)
    print "Process time developed: %d", time.time() - start
    start = time.time()
    imfs_2 = emdlib.emd(sine_wave, max_modes)
    print "Process time library: %d", time.time() - start
    plotter.plot_intrinsic_mode_functions(imfs, time_ax, 'Developed EMD', plt)
    plotter.plot_intrinsic_mode_functions(imfs_2, time_ax, 'Library EMD', plt)
    plt.show()
