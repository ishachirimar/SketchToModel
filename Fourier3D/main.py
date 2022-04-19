import ProbMat
import fourier3d as f3d


def create(i):
    dest = f3d.generate_compressed(
        "data/Test_Vox_0000.txt",  # Input data file.
        "f3d_out",  # Directory for output relative from content root.
        "spot_dissolve",  # Prefix of output file.
        i,  # All frequencies with an amplitude less than this --> 0.
        27,  # Model is saved in increments of 1/27th. Rounds to nearest, except all elements < 1/27 --> 0.
        # The string below is the necessary information for @ProbMat to parse back the model.
        "992.607296116719,384.94221438058,30.643160393146,0.983686369633562,0.179891984805166,0,-0.0980051161588621,"
        "0.535912130961478,0.838566148312115,-50,50,50"
    )
    print("Success: reformed model @ " + dest)


for i in range(0, 25):
    create(round(1250000/(100*i*i+1)-1))


quit()
