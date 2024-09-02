# extracts velocity data from an ODB file and writes it to two files, velocity_x.dat and velocity_y.dat

import numpy as np
from abaqusConstants import *
from odbAccess import *
from odbMaterial import *
from odbSection import *

# Open ODB
odb = openOdb(path="odb_filename.odb")

# Frames
fs = odb.steps["step_name"].frames

start_frame = 600

# Open files velocity_x.dat and velocity_y.dat in write mode
with open("velocity_x.dat", "w+") as vx_f, open("velocity_y.dat", "w+") as vy_f:
    # Iterate over frames in 'flow' step
    for i in range(start_frame, len(fs)):
        # Extract the velocity data for the current frame
        velocities = fs[i].fieldOutputs["V"].values

        # Pre-allocate lists for x and y velocities
        velxs = np.empty(len(velocities))
        velys = np.empty(len(velocities))

        # Populate the lists directly
        for j, velocity in enumerate(velocities):
            velxs[j], velys[j] = velocity.data[:2]

        # Write velocities to files
        np.savetxt(vx_f, velxs[None], delimiter=",", fmt="%f")
        np.savetxt(vy_f, velys[None], delimiter=",", fmt="%f")
