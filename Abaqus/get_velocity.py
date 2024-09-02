# extracts velocity data from an ODB file and writes it to two files, velocity_x.dat and velocity_y.dat

from abaqusConstants import *
from odbAccess import *
from odbMaterial import *
from odbSection import *

# Open ODB
odb = openOdb(path="odb_filename.odb")

# Frames
fs = odb.steps["step_name"].frames

START_FRAME = 400
END_FRAME = len(fs)

# Open files velocity_x.dat and velocity_y.dat in write mode
with open("velocity_x.dat", "w") as vx_f, open("velocity_y.dat", "w") as vy_f:
    for i in range(START_FRAME, END_FRAME):
        # Extract the velocity data for the current frame
        velocities = fs[i].fieldOutputs["V"].values

        # Use a generator expression to avoid creating intermediate arrays
        vx_f.write(
            ",".join(f"{velocity.data[0]:.6f}" for velocity in velocities) + "\n"
        )
        vy_f.write(
            ",".join(f"{velocity.data[1]:.6f}" for velocity in velocities) + "\n"
        )
