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

with open("velocity_x.dat", "w") as vx_f, open("velocity_y.dat", "w") as vy_f:
    for i in range(START_FRAME, END_FRAME):
        # Extract the velocity data for the current frame
        velocities = fs[i].fieldOutputs["V"].values

        # Use str.format() to format the output string
        vx_f.write(
            ",".join("{:.6f}".format(velocity.data[0]) for velocity in velocities)
            + "\n"
        )
        vy_f.write(
            ",".join("{:.6f}".format(velocity.data[1]) for velocity in velocities)
            + "\n"
        )
