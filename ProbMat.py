import matplotlib.pyplot as plt
import numpy as np
import os

class Grid:
    """ definition of a grid of points """

    def __init__(self):
        self.Origin = None
        self.XAxis = None
        self.YAxis = None
        self.Domain = None
        self.Count = None

class ProbabilityMatrix:
    """ a grid plus corresponding value matrix """

    def __init__(self, values, grid):
        self.Values = values
        self.Grid = grid


def readProbMat(path):
    """returns a [values matrix, grid info] pair"""
    print(path)
    file = open(path)
    txt = file.readlines()
    file.close()

    mygrid = Grid()
    grid_info = np.fromstring(txt.pop(), sep=",")

    mygrid.Origin = grid_info[0:3]
    mygrid.XAxis = grid_info[3:6]
    mygrid.YAxis = grid_info[6:9]
    mygrid.Domain = grid_info[9:11]
    mygrid.Count = int(grid_info[11])

    step = (mygrid.Domain[1] - mygrid.Domain[0]) / mygrid.Count
    phase = step / 2

    mat = np.zeros(pow(mygrid.Count, 3))
    for i in range(len(txt)):
        vals = txt[i][:-1].split(',')
        for j in range(len(vals)):
            mat[mygrid.Count * i + j] = float(vals[j])
    mat = mat.reshape(mygrid.Count, mygrid.Count, mygrid.Count)

    probmat = ProbabilityMatrix(mat, mygrid)

    return probmat


def dotplot(probmat, threshold, output=None):
    """Plot a dot representation of object in Camera Plane Space"""
    mat = probmat.Values
    grid = probmat.Grid

    b = mat < threshold
    mat[b] = 0

    step = (grid.Domain[1] - grid.Domain[0]) / grid.Count
    phase = step / 2

    fig = plt.Figure(figsize=(5, 5))
    ax = plt.axes(projection='3d')
    series = np.arange(grid.Domain[0]+phase, grid.Domain[1], step)
    print(series.size)
    xx, yy, zz = np.meshgrid(series, series, series)
    size = mat * 10
    ax.scatter(xx, yy, zz, c=mat, s=size)
    if output is not None:
        plt.savefig(output)
    plt.show()

def constructMesh(vertices, faces, path, name):
    """make an .OBJ file from point np.array with shape(n,3) and face index np.array with shape(n,4)"""
    txt = ""
    for v in vertices:
        txt += "v"
        for n in v:
            txt += " " + str(n)
        txt += "\n"

    for f in faces:
        txt += "f"
        for n in f:
            txt += " " + str(n)
        txt += "\n"

    file = open(path+name, 'w')
    file.write(txt)
    file.close()
    print("file made successfully here:\n" + path + name)
    return path + name


def meshprobmat(probmat, threshold, path, name, open):
    """convert the weighted voxel matrix into a mesh"""

    mat = probmat.Values
    grid = probmat.Grid

    step = (grid.Domain[1]-grid.Domain[0])/grid.Count
    phase = step/2

    # print(origin, xaxis, yaxis, domain, count, step)

    # get indices for each voxel as 3 lists
    series = np.arange(grid.Domain[0]+phase, grid.Domain[1], step)
    xx, yy, zz = np.meshgrid(series, series, series)

    # get vertex indices
    indices = np.arange(pow(grid.Count+1, 3)).reshape(grid.Count+1, grid.Count+1, grid.Count+1)
    indices = indices + 1

    # get  the world space coordinates for every vertex of the grid
    v_series = np.arange(grid.Domain[0], grid.Domain[1]+step, step)
    vx, vy, vz = np.meshgrid(v_series, v_series, v_series)
    vertices = np.stack((vx, vy, vz), axis=3)
    vertices = vertices.reshape(pow(grid.Count+1, 3), 3)

    # get boolean matrix by threshold
    mat_bool = mat > threshold

    # find left and right boundaries
    false_grid = np.full((1, grid.Count, grid.Count), False, dtype=bool)
    mat_left = np.concatenate((false_grid, mat_bool), 0)
    mat_right = np.concatenate((mat_bool, false_grid), 0)
    left_bool = np.logical_and(np.logical_not(mat_left), mat_right)
    left_bool = left_bool[:-1, :, :]
    right_bool = np.logical_and(mat_left, np.logical_not(mat_right))
    right_bool = right_bool[1:, :, :]

    left_faces_0 = indices[:-1, 1:, 1:][left_bool].flatten()
    left_faces_1 = indices[:-1, 1:, :-1][left_bool].flatten()
    left_faces_2 = indices[:-1, :-1, :-1][left_bool].flatten()
    left_faces_3 = indices[:-1, :-1, 1:][left_bool].flatten()
    print(left_faces_3.size)
    left_faces = np.column_stack((left_faces_3, left_faces_2, left_faces_1, left_faces_0))
    print(left_faces.shape)

    right_faces_0 = indices[1:, 1:, 1:][right_bool].flatten()
    right_faces_1 = indices[1:, 1:, :-1][right_bool].flatten()
    right_faces_2 = indices[1:, :-1, :-1][right_bool].flatten()
    right_faces_3 = indices[1:, :-1, 1:][right_bool].flatten()
    right_faces = np.column_stack((right_faces_0, right_faces_1, right_faces_2, right_faces_3))

    # find front and back boundaries
    false_grid = np.full((grid.Count, 1, grid.Count), False, dtype=bool)
    mat_front = np.concatenate((false_grid, mat_bool), 1)
    mat_back = np.concatenate((mat_bool, false_grid), 1)
    front_bool = np.logical_and(np.logical_not(mat_front), mat_back)
    front_bool = front_bool[:, :-1, :]
    back_bool = np.logical_and(mat_front, np.logical_not(mat_back))
    back_bool = back_bool[:, 1:, :]

    front_faces_0 = indices[1:, :-1, 1:][front_bool].flatten()
    front_faces_1 = indices[1:, :-1, :-1][front_bool].flatten()
    front_faces_2 = indices[:-1, :-1, :-1][front_bool].flatten()
    front_faces_3 = indices[:-1, :-1, 1:][front_bool].flatten()
    front_faces = np.column_stack((front_faces_0, front_faces_1, front_faces_2, front_faces_3))

    back_faces_0 = indices[1:, 1:, 1:][back_bool].flatten()
    back_faces_1 = indices[1:, 1:, :-1][back_bool].flatten()
    back_faces_2 = indices[:-1, 1:, :-1][back_bool].flatten()
    back_faces_3 = indices[:-1, 1:, 1:][back_bool].flatten()
    back_faces = np.column_stack((back_faces_3, back_faces_2, back_faces_1, back_faces_0))

    # find vertical boundaries by overlapping shifted matrices
    false_grid = np.full((grid.Count, grid.Count, 1), False, dtype=bool)
    mat_bot = np.concatenate((false_grid, mat_bool), 2)
    mat_top = np.concatenate((mat_bool,  false_grid), 2)
    bot_bool = np.logical_and(mat_top, np.logical_not(mat_bot))
    bot_bool = bot_bool[:, :, :-1]
    tops_bool = np.logical_and(np.logical_not(mat_top), mat_bot)
    tops_bool = tops_bool[:, :, 1:]

    bot_faces_0 = indices[1:, 1:, :-1][bot_bool].flatten()
    bot_faces_1 = indices[1:, :-1, :-1][bot_bool].flatten()
    bot_faces_2 = indices[:-1, :-1, :-1][bot_bool].flatten()
    bot_faces_3 = indices[:-1, 1:, :-1][bot_bool].flatten()
    bot_faces = np.column_stack((bot_faces_3, bot_faces_2, bot_faces_1, bot_faces_0))

    top_faces_0 = indices[1:, 1:, 1:][tops_bool].flatten()
    top_faces_1 = indices[1:, :-1, 1:][tops_bool].flatten()
    top_faces_2 = indices[:-1, :-1, 1:][tops_bool].flatten()
    top_faces_3 = indices[:-1, 1:, 1:][tops_bool].flatten()
    top_faces = np.column_stack((top_faces_0, top_faces_1, top_faces_2, top_faces_3))

    faces = np.row_stack((left_faces, right_faces, front_faces, back_faces, top_faces, bot_faces))
    print(vertices.shape)
    print(faces.shape)
    where = constructMesh(vertices, faces, path, name)

    if open:
        os.startfile(where)
