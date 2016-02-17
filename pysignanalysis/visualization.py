import utils
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


def plot_single_channel(sample_frequency, channel_data, plotter=plt, filename=str):
    plotter.ion()
    f, ax = plotter.subplots(1, 1)
    f.suptitle(filename)
    plotter.subplots_adjust(left=0.08, right=0.99, bottom=0.04, top=0.95, wspace=0.1, hspace=0.38)
    time_axis = scipy.linspace(start=0, stop=len(channel_data) / sample_frequency, num=len(channel_data))
    ylabel_str = "%s [%sV]" % ('EEG', u'\u00b5')
    ax.set_ylabel(ylabel_str)
    ax.set_xlabel('Time [s]')
    ax.plot(time_axis, channel_data)
    plotter.draw()


def plot_intrinsic_mode_functions(sample_frequency, imfs, channel=str, plotter=plt):
    n_rows = len(imfs)
    data_length = len(imfs[0])
    f, axis = plotter.subplots(n_rows, 1, sharex=True, sharey=False)
    time_axis = scipy.linspace(start=0, stop=data_length / sample_frequency, num=data_length)
    sup_title = "Channel " + channel
    f.suptitle(sup_title, fontsize=18)

    for i in range(n_rows):
        title = 'IMF: ' + str(i+1)
        axis[i].plot(time_axis, imfs[i])
        axis[i].set_title(title)
        axis[i].grid()
        # axis[i].set_ylim([-200, 200])

    axis[n_rows-1].set_xlabel('Time [s]')
    f.subplots_adjust(hspace=.5)


def plot_intrinsic_mode_functions_with_frequency_and_amplitude(sample_frequency, imfs, frequencies, amplitudes, channel=str, plotter=plt):
    n_rows = len(imfs)
    data_length = len(imfs[0])
    sup_title = "Channel " + channel
    f, axis = plotter.subplots(n_rows, 2, sharex=False, sharey=False)
    time_axis = scipy.linspace(start=0, stop=data_length / sample_frequency, num=data_length)
    f.suptitle(sup_title, fontsize=18)

    for i in range(0, n_rows):
        title = 'IMF: ' + str(i+1)
        axis[i][0].plot(time_axis, imfs[i])
        axis[i][0].set_title(title)
        axis[i][0].grid()
        axis[i][1].plot(frequencies[i], amplitudes[i])
        axis[i][1].set_ylabel('Amplitude')
        axis[i][1].grid()

    axis[n_rows - 1][0].set_xlabel('Time [s]')
    axis[n_rows - 1][1].set_xlabel('Frequency [Hz]')
    f.subplots_adjust(hspace=.5)


def plot_intrinsic_mode_functions_with_time_frequency_series(sample_frequency, imfs, frequencies, channel=str, plotter=plt):
    n_rows = len(imfs)
    data_length = len(imfs[0])
    sup_title = "Channel " + channel
    f, axis = plotter.subplots(n_rows, 2, sharex=False, sharey=False)
    time_axis = scipy.linspace(start=0, stop=data_length / sample_frequency, num=data_length)
    f.suptitle(sup_title, fontsize=18)

    for i in range(0, n_rows):
        title = 'IMF: ' + str(i+1)
        axis[i][0].plot(time_axis, imfs[i])
        axis[i][0].set_title(title)
        axis[i][0].grid()
        axis[i][1].plot(time_axis, frequencies[i])
        axis[i][1].set_ylabel('Frequency [Hz]')
        axis[i][1].grid()

    axis[n_rows - 1][0].set_xlabel('Time [s]')
    axis[n_rows - 1][1].set_xlabel('Time [s]')
    f.subplots_adjust(hspace=.5)


def plot_time_frequency_series(sample_frequency, frequencies, channel=str, plotter=plt):
    n_rows = len(frequencies)
    data_length = len(frequencies[0])
    sup_title = "Channel " + channel
    f, axis = plotter.subplots(n_rows, 1, sharex=False, sharey=False)
    time_axis = scipy.linspace(start=0, stop=data_length / sample_frequency, num=data_length)
    f.suptitle(sup_title, fontsize=18)

    for i in range(0, n_rows):
        title = 'IMF: ' + str(i+1)
        axis[i].plot(time_axis, frequencies[i])
        axis[i].set_title(title)
        axis[i].grid()

    axis[n_rows - 1].set_xlabel('Frequency [Hz]')
    axis[n_rows - 1].set_xlabel('Time [s]')
    f.subplots_adjust(hspace=.5)


def plot_original_signal_from_intrinsic_mode_functions(sample_frequency, imfs, residue, channel, plotter=plt):
    n_rows = len(imfs)
    data_length = len(imfs[0])
    final_signal = scipy.zeros(len(imfs[1]))
    time_axis = scipy.linspace(start=0, stop=data_length / sample_frequency, num=data_length)

    for i in range(n_rows):
        final_signal = scipy.add(final_signal, imfs[i + 1])

    final_signal = scipy.add(final_signal, residue)
    f, axis = plotter.subplots(1, 1)
    sup_title = "Channel " + channel
    f.suptitle(sup_title, fontsize=18)
    axis.plot(time_axis, final_signal)
    axis.grid()


def plot_hilbert_spectra_trisurf(sample_frequency, frequency, amplitude, plotter=plt, title=str):
    data_length = len(frequency[0])
    fig = plt.figure()
    time_axis = scipy.linspace(start=0, stop=data_length / sample_frequency, num=data_length)
    fig.suptitle(title)
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_trisurf(time_axis, frequency, amplitude, cmap=plotter.get_cmap('Spectral'), linewidth=1)
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


# FUNCTION FOR PLOTTING THE HILBERT SPECTRA FOR IMFs
def plot_hilbert_spectra(time, frequency, amplitude, title, plotter=plt, fs=100):

    # Scale factor (to plot frequency with decimal precision)
    scale_freq = 100
    # Max scaled frequency
    max_freq = int(0.5*scale_freq*fs)

    # Creating time axis
    time_ax = np.linspace(0, len(time)-1, len(time))
    # Allocating memory for power and the rounded frequency
    power_array = np.zeros(np.shape(frequency))
    freq_rounded_array = np.zeros(np.shape(power_array), np.int)

    # Create GRID based on time axis and maximum frequency
    yi = np.linspace(0, max_freq, max_freq + 1)
    Z = np.ones((max_freq + 1, len(time_ax)))*-200
    X, Y = np.meshgrid(time_ax, yi)

    # Enter loop if more than one IMF exists
    if isinstance(frequency[0], np.ndarray):

        for i in range(len(frequency)):

            # Normalize the amplitude ( 0<=a<=1)
            amplitude[i] = utils.normalize_data(amplitude[i])
            # Power equal to amplitude squared
            power_array[i] = np.multiply(amplitude[i], amplitude[i])
            # Round the frequency to the nearest (results in OK resolution if scale_freq > 1, eg scale_freq=10)
            freq_rounded_array[i] = np.ceil(frequency[i]*scale_freq)

            # Compute the logarithmic power, and add it to the previous if the same inst. frequency exists.
            for k in range(len(time_ax)):
                if power_array[i, k] == 0.0:
                        power_array[i, k] = 0.00000001
                current_amplitude = Z[int(freq_rounded_array[i, k]), int(time_ax[k])]
                if current_amplitude > -200:
                    Z[int(freq_rounded_array[i, k]), int(time_ax[k])] = current_amplitude + 20.0*np.log10(power_array[i, k])
                else:
                    Z[int(freq_rounded_array[i, k]), int(time_ax[k])] = 20.0*np.log10(power_array[i, k])
    else:

        # Normalize the amplitude ( 0<=a<=1)
        amplitude = utils.normalize_data(amplitude)
        # Power equal to amplitude squared
        power_array = np.multiply(amplitude, amplitude)
        # Round the frequency to the nearest (results in OK resolution if scale_freq > 1, eg scale_freq=10)
        freq_rounded_array = np.ceil(frequency*scale_freq)
        # Compute the logarithmic power, and add it to the previous if the same inst. frequency exists.
        for k in range(len(time_ax)):
            Z[int(freq_rounded_array[k]), int(time_ax[k])] = 20.0*np.log10(power_array[k])

    # Create figure and subplot.
    # Set titles and labels.
    fig = plotter.figure()
    suptitle = 'Hilbert Spectra - Channel: ' + title
    fig.suptitle(suptitle)
    ax = plotter.subplot(111)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Frequency [Hz]')

    # Create contour plot og time, frequency and logarithmic power. Scale frequencies back to original values.
    n_levels = 200
    cax = ax.contourf(X, Y/scale_freq, Z, n_levels)
    # Assign color bar to the contour plot
    cb = fig.colorbar(cax)
    # Set label and draw plot
    cb.set_label('Amplitude [dB]')
    plotter.draw()


def plot_scalp_spectra():
    return 0


