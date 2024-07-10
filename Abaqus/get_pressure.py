# Extract pressure data from an Abaqus ODB file and write it to a file

from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
import numpy as np

# Open ODB
odb = openOdb(path='odb_filename.odb')

# Frames
fs = odb.steps['step_name'].frames # name of the step

start_frame = 600

# Open a file pressure.dat in write mode
with open('pressure.dat', 'w+') as f:
    # Create a list of pressure values for each frame
    pressures = [[pressure.data for pressure in fs[i].fieldOutputs['PRESSURE'].values] for i in range(start_frame, len(fs))]
    # Write pressures to file
    np.savetxt(f, pressures, delimiter=',')
