import numpy as np
from scipy.fft import ifftn, fftn

import ProbMat
from interpreter import parse


def model(file_path, np_3d_array, post_mark=""):
    """Saves the model in [np_3d_array] to the destination [file_path]. Overwrites."""
    fileout = open(file_path, "w")
    for i in range(0, len(np_3d_array)):
        for j in range(0, len(np_3d_array[i])):
            for k in range(0, len(np_3d_array[i][j])):
                append_me = str(np.real(np_3d_array[i][j][k]))
                if k != len(np_3d_array) - 1:
                    append_me = append_me + ","
                fileout.write(append_me)
            fileout.write("\n")
    fileout.write(post_mark)


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
                        model_fractional=27, post_mark=""):
    """Given .otto data at [file_path], writes a compressed version of the model, quashing amplitudes
    less than [freq_floor], to [output_directory] with the name "[output_prefix]_[flooring].txt".
    [model_fractional] determines the model's voxel quantization (voxel transparency).
    [decimal_rounding] determines how many decimal places are saved.
        <!> [decimal_rounding] be redundant with [model_fractional] -- merge.
    :returns string representing output file location
    """
    sampledata = ProbMat.readProbMat(file_path).Values

    series = fftn(sampledata)
    reduce(series, int(freq_floor))  # Destructively modifies series to keep high-amplitude components.

    recovered_model = quash_below(ifftn(series), (1 / model_fractional))
    # Inverses Transform, elements < model_fractional --> 0.
    round_model(recovered_model, model_fractional)

    model(str(output_directory) + "/" + str(output_prefix) + "/" + str(freq_floor) + ".txt", recovered_model, post_mark)
    return str(output_directory) + "/" + str(output_prefix) + "/" + str(freq_floor) + ".txt"


def single_freq_eval(size, i, j, k, x, y, z, amp_real, amp_complex):
    """
    :returns: the result of the 3d-frequency <i,j,k> evaluated at <x,y,z>.
    """
    tpi = 2 * np.pi
    val = (-1) * amp_complex * np.sin(tpi * (i * x + j * y + k * z) / size) + amp_real * np.cos(
        tpi * (i * x + j * y + k * z) / size)
    return val * (1 / (size ** 3))
    # Adjustments: shrunk by size^-3, amp_complex applies to sin, amp_real applies to cos, (-1) amp_complex


def evaluate_at(np_3d_array_frequencies, x, y, z):
    """
    :return: The fourier series evaluated at the point (x,y,z)
    """
    sz = len(np_3d_array_frequencies)
    val = 0
    for i in range(0, sz):
        for j in range(0, sz):
            for k in range(0, sz):
                amp_real = np.real(np_3d_array_frequencies[i][j][k])
                amp_complex = np.imag(np_3d_array_frequencies[i][j][k])
                val += single_freq_eval(sz, i, j, k, x, y, z, amp_real, amp_complex)
                # print(val)
    return val


# Save as list of (3, s3) of [i=[],j=[],k=[]]
def evaluate_with_matrix(np_3d_array_frequencies,xyz):
    size = len(np_3d_array_frequencies)
    s3 = size ** 3

    i = np.linspace(0, size - 1, size)

    A = np.array(np.meshgrid(i, i, i))
    A = A.reshape(3, s3)  # Flatten into list of frequencies. (3x8000)

    A_freq = np_3d_array_frequencies.reshape(1, s3)  # List of complex numbers. (1x8000)
    # print(A.shape,A_freq.shape)

    print(A.shape,xyz.shape)
    M = np.matmul(A.T, xyz)
    np.multiply((2 * np.pi / size), M,out=M)

    return np.ndarray.flatten(-np.imag(A_freq) @ np.sin(M) + np.real(A_freq) @ np.cos(M))/s3


"""
M list comprehension


"""
