import time
import numpy as np
import fourier3d as f3d
from scipy.fft import ifftn, fftn
import interpreter as intp

print("RUNNING:")

out = "Fourier3D/f3d_out/"

####################################
# Just instantiating different tests.
####################################
sz = 50
tester = np.zeros([sz, sz, sz], dtype=complex)
freq_null = ifftn(tester)

tester[0][0][1] = 1 - 1j
freq_z = ifftn(tester)

tester[0][0][1] = 0  # Clean to zeroes
tester[0][1][0] = 1
freq_y = ifftn(tester)

tester[0][1][0] = 0  # Clean to zeroes
tester[1][0][0] = 1
freq_x = ifftn(tester)

tester[1][0][0] = 0  # Clean to zeroes
tester[1][1][1] = 1
freq_1_1_1 = ifftn(tester)

tester[1][1][1] = 0  # Clean to zeroes
tester[1][2][4] = 1 + 2j
hard_test = ifftn(tester)

tester = np.zeros([sz, sz, sz], dtype=complex)
tester[15][27][3] = 15
tester[12][37][25] = 10
tester[10][5][1] = 15
tester[1][3][2] = 20
multi_freq = ifftn(tester)
####################################
ref = open("f3d_out/ref_out.txt", "w")
des = open("f3d_out/des_out.txt", "w")

ref.write("L = [")
for i in range(0, sz):
    strb = str(np.real(hard_test[i][int(i/2)][int(i/3)])*(sz**3))
    # It appears the amplitudes ARE scaled by total number of them.
    ref.write(strb)
    if i != sz-1:
        ref.write(",")
ref.write("]")
ref.close()

des.write("D = [")
for i in range(0, sz):                    # sz, i, j, k, x, y, z,sA,cA
    strb = str(np.real(f3d.single_freq_eval(sz, 1, 2, 4, i, int(i/2), int(i/3), 1, 2))*(sz**3))
    des.write(strb)
    if i != sz-1:
        des.write(",")
des.write("]")
des.close()

spot = intp.parse("data/Spot_01.txt")
ifty = time.time_ns()
print("IFFTN -->" + str(np.real(ifftn(spot)[27][27][2])))
ifty = time.time_ns() - ifty
print("time of IFFTN = "+str(ifty)+"ns")

mat = time.time_ns()
print("MATR@ -->" + str(f3d.evaluate_with_matrix(spot, np.array(([27]*(10**3), [27]*(10**3), [2]*(10**3))))[0]))
mat = time.time_ns() - mat
print("time of MATR@ = "+str(mat/(10**9))+"s")

eval = time.time_ns()
print("EVAL@ -->" + str(f3d.evaluate_at(spot, 27, 27, 2)))
eval = time.time_ns() - eval
print("time of EVAL@ = "+str(eval)+"ns")

print("CONCLUDED:")