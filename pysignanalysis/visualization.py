import scipy
import numpy as np
import matplotlib.pyplot as plt


tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]


def get_color_for_channel(json_data):
    channel_color = {}
    color_table = np.ndarray(np.shape(tableau20))

    for i in range(len(color_table)):
        r, g, b = tableau20[i]
        color_table[i] = (r / 255., g / 255., b / 255.)

    i = 0

    for key, value in json_data.items():
        channel_color[key] = color_table[i]
        i += 1

    return channel_color


def plot_single_channel(ch_data, my_plot=plt, filename=str):
    my_plot.ion()
    f, ax = my_plot.subplots(1, 1)
    f.suptitle(filename)
    my_plot.subplots_adjust(left=0.08, right=0.99, bottom=0.04, top=0.95, wspace=0.1, hspace=0.38)
    time_axis = scipy.linspace(start=0, stop=len(ch_data) / 250, num=len(ch_data))
    ylabel_str = "%s [%sV]" % ('EEG', u'\u00b5')
    ax.set_ylabel(ylabel_str)
    ax.set_xlabel('Time [s]')
    ax.plot(time_axis, ch_data)
    my_plot.draw()


def plot_intrinsic_mode_functions(imfs, time_axis, channel=str, plotter=plt):
    n_rows = len(imfs)
    f, axis = plotter.subplots(n_rows, 1, sharex=True, sharey=False)
    sup_title = "Channel " + channel
    f.suptitle(sup_title, fontsize=18)

    for i in range(n_rows):
        title = 'IMF: ' + str(i+1)
        axis[i].plot(time_axis, imfs[i])
        axis[i].set_title(title)
        axis[i].grid()

    axis[n_rows-1].set_xlabel('Time [s]')
    f.subplots_adjust(hspace=.5)


def plot_intrinsic_mode_functions_with_frequency_and_amplitude(imfs, time_axis, freq_array, amp_array,
                                                               channel=str, plotter=plt):
    n_rows = len(imfs)
    sup_title = "Channel " + channel
    f, axis = plotter.subplots(n_rows, 2, sharex=False, sharey=False)
    f.suptitle(sup_title, fontsize=18)

    for i in range(0, n_rows):
        title = 'IMF: ' + str(i+1)
        axis[i][0].plot(time_axis, imfs[i])
        axis[i][0].set_title(title)
        axis[i][0].grid()
        axis[i][1].plot(time_axis, freq_array[i])
        axis[i][1].set_ylabel('Amplitude')
        axis[i][1].grid()
    axis[n_rows - 1][0].set_xlabel('Time [s]')
    axis[n_rows - 1][1].set_xlabel('Frequency [Hz]')
    f.subplots_adjust(hspace=.5)


def plot_original_signal_from_intrinsic_mode_functions(imfs, residue, time_axis, channel, plotter=plt):
    n_rows = len(imfs)
    final_signal = scipy.zeros(len(imfs[1]))

    for i in range(n_rows):
        final_signal = scipy.add(final_signal, imfs[i + 1])

    final_signal = scipy.add(final_signal, residue)
    f, axis = plotter.subplots(1, 1)
    sup_title = "Channel " + channel
    f.suptitle(sup_title, fontsize=18)
    axis.plot(time_axis, final_signal)
    axis.grid()


def plot_hilbert_spectra_trisurf(time, frequency, amplitude, plotter=plt, title=str):
    fig = plt.figure()
    fig.suptitle(title)
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_trisurf(time, frequency, amplitude, cmap=plotter.get_cmap('Spectral'), linewidth=1)
    fig.colorbar(surf)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Frequency [Hz]')
    ax.set_zlabel('Amplitude')
    fig.tight_layout()


def plot_power_spectral_density(frequency, amplitude, plotter=plt, title=str):
    fig = plotter.figure()
    ax = fig.add_subplot(111)
    fig.suptitle(title)
    power = np.multiply(amplitude, amplitude)
    ax.plot(frequency, power)
    ax.set_xlabel('Frequency [Hz]')
    ylabel = 'Power Spectral Density [%sV^2]' % u'\u00b5'
    ax.set_ylabel(ylabel)
    plotter.draw()


