import numpy as np
import scipy.signal as signal
import scipy.interpolate as interpolate


def emd(x, max_modes=5):
    imfs = np.ndarray((max_modes, len(x)))
    n = 0
    N = max_modes
    residue = x

    while n <= N - 1:
        imf = sift_process(residue)
        imfs[n] = imf
        n += 1
        residue = residue - imf
        # if n >= 2:
        #     std = get_imf_std_deviation(imfs[n-2], imfs[n-1])
        #     print "STD = ", std
        #     if 0.2 <= std <= 0.3:
        #         break

    return imfs


def sift_process(residue):
    mode = residue
    max_siftings = 100
    n_siftings = 0

    while n_siftings < max_siftings - 1:
        mode = sift_one(mode)
        extrema, zero_crossings, mean = analyze_mode(mode)
        n_siftings += 1
        if abs(extrema - zero_crossings) <= 1 and -0.001 <= mean <= 0.001:
            break

    return mode


def sift_one(mode):
    maxima = find_maxima(mode)
    minima = find_minima(mode)
    upper_signal = interpolate_maxima(mode, maxima)
    lower_signal = interpolate_minima(mode, minima)
    mean = find_local_mean(lower_signal, upper_signal)
    return mode - mean


def find_minima(x):
    return signal.argrelextrema(x, np.less)[0]


def find_maxima(x):
    return signal.argrelextrema(x, np.greater)[0]


def analyze_mode(mode):
    maxima = signal.argrelextrema(mode, np.greater)
    minima = signal.argrelextrema(mode, np.less)
    extrema = np.size(maxima) + np.size(minima)
    zero_crossings = find_number_of_zero_crossings(mode)
    return extrema, zero_crossings, np.mean(mode)


def find_local_mean(lower_signal, upper_signal):
    sum_arr = np.add(lower_signal, upper_signal)
    return np.multiply(sum_arr, 0.5)


def find_number_of_zero_crossings(x):
    crossings = len(np.where(np.diff(np.signbit(x)))[0])
    return crossings


def get_imf_std_deviation(imf_old, imf_new):
    abs_diff = np.abs(np.subtract(imf_old, imf_new))
    return np.std(abs_diff)


def interpolate_maxima(x, maxima):
    t = np.arange(0, len(x))
    size = np.size(maxima)

    if size == 0:
        return np.ones(len(x)) * 0

    if size == 1:
        return np.ones(len(x)) * x[maxima]

    points, maxima = correct_end_effects(x, maxima, True)
    tck = interpolate.splrep(maxima, points)
    return interpolate.splev(t, tck)


def interpolate_minima(x, minima):
    t = np.arange(0, len(x))
    size = np.size(minima)

    if size == 0:
        return np.ones(len(x)) * 0

    if size == 1:
        return np.ones(len(x)) * x[minima]

    points, minima = correct_end_effects(x, minima, False)
    tck = interpolate.splrep(minima, points)
    return interpolate.splev(t, tck)


def correct_end_effects(x, extrema, is_maxima):
    interpolation_points = x[extrema]
    start_point = get_start_point_from_linear_spline_of_two_extrema_near_boundary(x, extrema)
    end_point = get_end_point_from_linear_spline_of_two_extrema_near_boundary(x, extrema)
    interpolation_points, extrema = add_end_point_to_interpolation(x, interpolation_points, extrema, end_point, is_maxima)
    interpolation_points, extrema = add_start_point_to_interpolation(x, interpolation_points, extrema, start_point, is_maxima)
    return interpolation_points, extrema


def get_end_point_from_linear_spline_of_two_extrema_near_boundary(x, extrema):
    slope = (x[extrema[-1]] - x[extrema[-2]]) / (extrema[-1] - extrema[-2])
    dt = len(x) - extrema[-1]
    return slope * dt + x[extrema[-1]]


def get_start_point_from_linear_spline_of_two_extrema_near_boundary(x, extrema):
    slope = (x[extrema[0]] - x[extrema[1]]) / (extrema[0] - extrema[1])
    dt = extrema[1]
    return slope * dt + x[extrema[1]]


def add_end_point_to_interpolation(x, interpolation_points, extrema, end_point, is_maxima):
    if is_maxima:
        return add_end_point_as_maxima(x, interpolation_points, extrema, end_point)
    else:
        return add_end_point_as_minima(x, interpolation_points, extrema, end_point)


def add_start_point_to_interpolation(x, interpolation_points, extrema, start_point, is_maxima):
    if is_maxima:
        return add_start_point_as_maxima(x, interpolation_points, extrema, start_point)
    else:
        return add_start_point_as_minima(x, interpolation_points, extrema, start_point)


def add_end_point_as_maxima(x, interpolation_points, extrema, end_point):
    length_of_data = len(x)-1
    if end_point < x[length_of_data]:
        interpolation_points = np.append(interpolation_points, [x[length_of_data]])
        extrema = np.append(extrema, [length_of_data])
    else:
        np.append(interpolation_points, [end_point])
        np.append(extrema, [length_of_data])
    return interpolation_points, extrema


def add_end_point_as_minima(x, interpolation_points, extrema, end_point):
    length_of_data = len(x)-1
    if end_point < x[length_of_data]:
        interpolation_points = np.append(interpolation_points, [end_point])
        extrema = np.append(extrema, [length_of_data])
    else:
        interpolation_points = np.append(interpolation_points, [x[length_of_data]])
        extrema = np.append(extrema, [length_of_data])
    return interpolation_points, extrema


def add_start_point_as_maxima(x, interpolation_points, extrema, start_point):
    if start_point < x[0]:
        interpolation_points = np.insert(interpolation_points, [0], [x[0]])
        extrema = np.insert(extrema, [0], [0])
    else:
        interpolation_points = np.insert(interpolation_points, [0], [start_point])
        extrema = np.insert(extrema, [0], [0])
    return interpolation_points, extrema


def add_start_point_as_minima(x, interpolation_points, extrema, start_point):
    if start_point < x[0]:
        interpolation_points = np.insert(interpolation_points, [0], [start_point])
        extrema = np.insert(extrema, [0], [0])
    else:
        interpolation_points = np.insert(interpolation_points, [0], [x[0]])
        extrema = np.insert(extrema, [0], [0])
    return interpolation_points, extrema
