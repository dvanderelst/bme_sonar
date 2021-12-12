import numpy
import os
from ReadSettings import SettingsReader
from scipy.interpolate import interp1d
from matplotlib import pyplot
from scipy.io.wavfile import write
from scipy.signal import chirp, find_peaks
import subprocess

Settings = SettingsReader()

def measurement2wav(file_name):
    cut_off = 250
    bat_ping_duration = 0.0025
    time_expansion_factor = 200
    wav_fs = 44100
    start_f = 7500
    end_f = 2000

    data = numpy.loadtxt(file_name)

    data = data - cut_off
    data[data < 0] = 0
    rate = Settings.rate

    samples = len(data)
    duration = time_expansion_factor * (samples/ rate)
    time_stamps = numpy.linspace(0,duration, samples)
    interpolation_time_stamps = numpy.arange(0, duration, 1/wav_fs)

    interpolation_function = interp1d(time_stamps, data)
    interpolated_data = interpolation_function(interpolation_time_stamps)

    result = find_peaks(interpolated_data)
    peak_x = interpolation_time_stamps[result[0]]
    peak_y = interpolated_data[result[0]]


    ping_duration = bat_ping_duration * time_expansion_factor
    ping_time_stamps = numpy.arange(0, ping_duration, 1/wav_fs)
    ping = chirp(ping_time_stamps, start_f, ping_duration, end_f, method='hyperbolic')
    window = numpy.hanning(len(ping))
    ping = ping * window

    impulse_response = numpy.zeros(len(interpolated_data))
    impulse_response[result[0]] = peak_y
    impulse_response[0] = numpy.max(data)

    wave = numpy.convolve(impulse_response, ping, mode='same')

    pyplot.plot(interpolation_time_stamps, interpolated_data)
    pyplot.scatter(peak_x, peak_y)
    pyplot.title('Recorded wave with selected peaks')
    pyplot.show()

    pyplot.plot(interpolation_time_stamps, wave)
    pyplot.title('Reconstructed waveform')
    pyplot.show()

    scaled = numpy.int16(wave / numpy.max(numpy.abs(wave)) * 32767)
    write('reconstructed.wav', wav_fs, scaled)


if __name__ == "__main__":
    selected_index = 5

    buffer_files = os.listdir('buffer')
    for i,f in enumerate(buffer_files): print(i, f)

    selected_file = buffer_files[selected_index]
    print('Selected file:', selected_file)

    selected_file = os.path.join('buffer', selected_file)
    measurement2wav(selected_file)




