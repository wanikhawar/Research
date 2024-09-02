# Extract pressure data from an Abaqus ODB file and write it to a file

from abaqusConstants import *
from odbAccess import *
from odbMaterial import *
from odbSection import *

# Open ODB
odb = openOdb(path="odb_filename.odb")

# Frames
fs = odb.steps["step_name"].frames  # name of the step

START_FRAME = 600
END_FRAME = len(fs)

with open("pressure.dat", "w") as f:
    for i in range(START_FRAME, END_FRAME):
        # Extract the pressure data for the current frame
        pressures = fs[i].fieldOutputs["PRESSURE"].values

        print("WRITING STEP {0} DATA".format(i))

        # Write pressures to file
        f.write(
            ",".join("{:.6f}".format(pressure.data) for pressure in pressures) + "\n"
        )
