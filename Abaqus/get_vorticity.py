from abaqusConstants import *
from odbAccess import *
from odbMaterial import *
from odbSection import *

# Open ODB
odb = openOdb(path="odb_filename.odb")

# Frames
fs = odb.steps["step_name"].frames

START_FRAME = 600
END_FRAME = len(fs)

with open("vorticity_x.dat", "w") as vortx_f, open(
    "vorticity_y.dat", "w"
) as vorty_f, open("vorticity_z.dat", "w") as vortz_f:
    for i in range(START_FRAME, END_FRAME):
        # Extract the vorticity data for the current frame
        vorticities = fs[i].fieldOutputs["VORTICITY"].values

        print("WRITING STEP {0} DATA".format(i))

        # Write vorticities to files
        vortx_f.write(
            ",".join("{:.6f}".format(vorticity.data[0]) for vorticity in vorticities)
            + "\n"
        )
        vorty_f.write(
            ",".join("{:.6f}".format(vorticity.data[1]) for vorticity in vorticities)
            + "\n"
        )
        vortz_f.write(
            ",".join("{:.6f}".format(vorticity.data[2]) for vorticity in vorticities)
            + "\n"
        )
