import ProbMat

path = "C:\\Users\\smbry\\Desktop\\SketchToModel\\Fourier3D\\f3d_out\\spot_dissolve\\"
figpath = "C:\\Users\\smbry\\Desktop\\SketchToModel\\Fourier3D\\f3d_out\\spot_plots\\14_27\\"
name = "21.txt"

"read file returns a [value matrix, grid] pair"
myprobmat = ProbMat.readProbMat(path + name)

ProbMat.dotplot(myprobmat, 0, figpath)

sequence_files = [21, 23, 25, 27, 30, 34, 38, 42, 48, 55, 63, 73, 86, 102, 124, 153, 194, 254, 346, 499, 780, 1386,
                  3116, 12375]

for i in range(0, len(sequence_files)):
    myprobmat = ProbMat.readProbMat(path + str(sequence_files[i])+".txt")
    ProbMat.dotplot(myprobmat, 14/27, figpath+str(i+1)+".png")

quit()
