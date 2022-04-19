import ProbMat

path = "C:\\Users\\jackm\Documents\\Cornell 21-22\\2_ITHACA\\SketchToModel\\TrainingData\\Voxels\\"
name = "Test_Vox_0000.txt"

"read file returns a [value matrix, grid] pair"
myprobmat = ProbMat.readProbMat(path+name)
print(myprobmat.Values)
print(myprobmat.Grid)

ProbMat.dotplot(myprobmat, 0)

path = "C:\\Users\\jackm\Documents\\Cornell 21-22\\2_ITHACA\\SketchToModel\\"
name = "myobjtest.obj"
ProbMat.meshprobmat(myprobmat, .25, path, name, True)
