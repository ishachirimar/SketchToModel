import numpy as np


def to_np(parsed_data):
    """
    Helper function for [@parse]. Converts parsed_data from a 3-Dimensional array to a 3-Dimensional numpy array.
    requires: [parsed_data] is a rectangular prism, i.e., all parallel slices have same dimensions.
    """
    fill_me = np.zeros((len(parsed_data), len(parsed_data[0]), len(parsed_data[0][0])))
    for i in range(0, len(parsed_data)):
        for j in range(0, len(parsed_data[i])):
            for k in range(0, len(parsed_data[i][j])):
                fill_me[i][j][k] = parsed_data[i][j][k]
    return fill_me


def string_to_float(np_3d_array):
    """
    Helper function for [@parse]. Converts the messy, stringy newline clutter into 3d float list.
    """
    outer_array = []
    for i in range(0, len(np_3d_array)):
        middle_array = []
        for j in range(0, len(np_3d_array[i])):
            builder_array = []
            for k in range(0, len(np_3d_array[i][j])):
                current_item = np_3d_array[i][j][k]
                if not("\n" in current_item):
                    if current_item:
                        builder_array = builder_array + [float(current_item)]
                else:
                    maybe = current_item.split("\n")[0]
                    if maybe:
                        builder_array = builder_array + [float(maybe)]
                        middle_array = middle_array + [builder_array]
        outer_array = outer_array + [middle_array]
    return outer_array


def parse(file_path):
    """Parses a .otto file into a 3-Dimensional array.
    Example:
        0.0, 1.0    # .otto format
        2.0, 3.0

        0.1, 1.1
        2.1, 3.1
        ->
        [[[0.0,1.0],[2.0,3.0]],[[0.1,1.1],[2.1,3.1]]]  # output format
    """
    file = open(file_path, "r")
    cur_line = None
    liner = []
    blocker = []
    while cur_line != "":
        cur_line = file.readline()
        if cur_line != "\n":
            arr = cur_line.split(", ")
            liner = liner + [arr]
        else:
            blocker = blocker + [liner]
            liner = []
    blocker = blocker + [liner]
    return to_np(string_to_float(blocker))
