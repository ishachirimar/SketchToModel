import numpy as np
from scipy.fft import ifftn, fftn
from interpreter import parse


def model(file_path, np_3d_array):
    """Saves the model in [np_3d_array] to the destination [file_path]. Overwrites."""
    fileout = open(file_path, "w")
    for i in range(0, len(np_3d_array)):
        for j in range(0, len(np_3d_array[i])):
            for k in range(0, len(np_3d_array[i][j])):
                fileout.write(str(np.real(np_3d_array[i][j][k])) + " ")
            fileout.write("\n")
        fileout.write("\n")


def round_model(np_3d_array, frac_steps):
    """Rounds elements in [np_3d_array] according to [frac_steps]. 3 means round-to-nearest-third.
    For traditional rounding (truncating by decimal place), use a power of 10.
    """
    for i in range(0, len(np_3d_array)):
        for j in range(0, len(np_3d_array[i])):
            for k in range(0, len(np_3d_array[i][j])):
                np_3d_array[i][j][k] = round(frac_steps * np.real(np_3d_array[i][j][k])) / frac_steps


def frequencies(file_path, np_3d_array_complex):
    """Saves the in [np_3d_array_complex] to the destination [file_path]. Overwrites.
    [frac_steps] determines the rounding; 3 means round-to-nearest-third. For traditional
    rounding (truncating by decimal place), use a power of 10.
    """
    fileout = open(file_path)
    for i in range(0, len(np_3d_array_complex)):
        for j in range(0, len(np_3d_array_complex[i])):
            for k in range(0, len(np_3d_array_complex[i][j])):
                fileout.write(str((np_3d_array_complex[i][j][k])) + " ")
            fileout.write("\n")
        fileout.write("\n")


def reduce(np_3d_array_complex, flooring):
    """Sets all frequencies with magnitudes less than 0 in [np_3d_array_complex] to 0."""
    for i in range(0, len(np_3d_array_complex)):
        for j in range(0, len(np_3d_array_complex[i])):
            for k in range(0, len(np_3d_array_complex[i][j])):
                if np.abs(np_3d_array_complex[i][j][j]) < flooring:
                    np_3d_array_complex[i][j][k] = 0 + 0j


def reduce_predict(np_3d_array_complex, flooring):
    """Counts how many frequencies in [np_3d_array_complex]
    have magnitudes greater than [flooring]."""
    counter = 0
    total = 0
    for i in range(0, len(np_3d_array_complex)):
        for j in range(0, len(np_3d_array_complex[i])):
            for k in range(0, len(np_3d_array_complex[i][j])):
                if np.abs(np_3d_array_complex[i][j][j]) < flooring:
                    counter += 1
                total += 1
    return total - counter


def quash_below(np_3d_array, flooring):
    """Sets all elements below the threshold [flooring] in [np_3d_array] to 0."""
    for i in range(0, len(np_3d_array)):
        for j in range(0, len(np_3d_array[i])):
            for k in range(0, len(np_3d_array[i][j])):
                if np_3d_array[i][j][k] < flooring:
                    np_3d_array[i][j][k] = 0
    return np_3d_array


def reduction_spectrum(np_3d_array_complex, start, end, res, file_path):
    """Where [start] and [end] represent frequency-amplitude thresholds,
    [reduction_spectrum] Subdivides the range [start,end] into [res]-many segments and evaluates
    how many frequencies are still pronounced. Outputs to [file_path]. Overwrites.
    """
    fileout = open(file_path, "w")
    ar = np.zeros(end - start)
    for i in range(0, res):
        x = start + i * (end - start) / res
        ar[i] = reduce_predict(np_3d_array_complex, x)
        fileout.write("(" + str(x) + "," + str(ar[i]) + "),")
    return ar


def generate_compressed(file_path, output_directory="data", output_prefix="model", freq_floor=0,
                        model_fractional=27):
    """Given .otto data at [file_path], writes a compressed version of the model, quashing amplitudes
    less than [freq_floor], to [output_directory] with the name "[output_prefix]_[flooring].txt".
    [model_fractional] determines the model's voxel quantization (voxel transparency).
    [decimal_rounding] determines how many decimal places are saved.
        <!> [decimal_rounding] be redundant with [model_fractional] -- merge.
    :returns string representing output file location
    """
    sampledata = parse(file_path)

    series = fftn(sampledata)
    reduce(series, int(freq_floor))  # Destructively modifies series to keep high-amplitude components.

    recovered_model = quash_below(ifftn(series), (1 / model_fractional))
    # Inverses Transform, elements < model_fractional --> 0.
    round_model(recovered_model, model_fractional)

    model(str(output_directory) + "/" + str(output_prefix) + "_" + str(freq_floor) + ".txt", recovered_model)
    return str(output_directory) + "/" + str(output_prefix) + "_" + str(freq_floor) + ".txt"


quit()
