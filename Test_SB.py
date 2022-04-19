import ProbMat

path = "C:\\Users\\smbry\\Desktop\\SketchToModel\\Fourier3D\\f3d_out\\spot_dissolve"
name = "SpotOut_8000_2.txt"

"read file returns a [value matrix, grid] pair"
myprobmat = ProbMat.readProbMat(path + name)
print(myprobmat.Values)
print(myprobmat.Grid)

ProbMat.dotplot(myprobmat, 0)

# path = "C:\\Users\\jackm\\Documents\\Cornell 21-22\\2_ITHACA\\SketchToModel\\"
# name = "myobjtest.obj"
# ProbMat.meshprobmat(myprobmat, .25, path, name, True)
