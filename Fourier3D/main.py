import fourier3d

dest = fourier3d.generate_compressed(
    "data/Spot_01.txt",  # Input data file.
    "data",  # Directory for output relative from content root.
    "spot",  # Prefix of output file.
    0,  # All frequencies with an amplitude less than this --> 0.
    27  # Model is saved in increments of 1/27th. Rounds to nearest, except all elements < 1/27 --> 0.
)

print("Success: reformed model @ " + dest)

quit()
