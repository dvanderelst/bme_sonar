import numpy
from matplotlib import pyplot

from ReadSettings import SettingsReader


def get_distance_axis(data):
    settings = SettingsReader()
    rate = settings.rate
    max_time = 1000 * len(data) / rate
    distance_axis = numpy.linspace(0, max_time, len(data)) * 17
    return distance_axis


def process_data_for_plotting(raw_data, raw=False, plot=False):
    settings = SettingsReader()
    threshold = settings.signal_threshold
    baseline = settings.baseline

    above_threshold = numpy.where(raw_data > threshold)[0]
    first_above_threshold = numpy.min(above_threshold)

    new_data = raw_data * 1.0
    if not raw:
        new_data = new_data[first_above_threshold + 1:]
        new_data = new_data - baseline

    distance_axis = get_distance_axis(new_data)

    if plot:
        length = len(raw_data)
        pyplot.subplot(1, 2, 1)
        pyplot.plot(raw_data)
        pyplot.hlines(baseline, 0, length, 'g')
        pyplot.hlines(threshold, 0, length, 'r')
        pyplot.scatter(first_above_threshold, raw_data[first_above_threshold], color='orange')
        pyplot.xlabel('Sample')
        pyplot.subplot(1, 2, 2)
        pyplot.plot(distance_axis, new_data)
        pyplot.xlabel('Distance [cm]')
        pyplot.show()
    return distance_axis, new_data


if __name__ == "__main__":
    test_data = 'buffer/measurement_0000_savethis.txt'
    stored_data = numpy.loadtxt(test_data)
    dist, new = process_data_for_plotting(stored_data, raw=True, plot=True)
