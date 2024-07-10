# extracts vorticity data from an ODB file and writes it to three files, vorticity_x.dat, vorticity_y.dat, and vorticity_z.dat

from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
import numpy as np

# Open ODB
odb = openOdb(path='odb_filename.odb')

# Frames
fs = odb.steps['step_name'].frames

start_frame = 600

# Open files velocity_x.dat and velocity_y.dat in write mode
with open('vorticity_x.dat', 'w+') as vortx_f, open('vorticity_y.dat', 'w+') as vorty_f, open('vorticity_z.dat', 'w+') as vortz_f:
    # Iterate over frames in 'flow' step
    for i in range(start_frame, len(fs)):
        # Create dictionary of node labels and x, y, and z vorticities
        vort = {vorticity.nodeLabel: vorticity.data[:3] for vorticity in fs[i].fieldOutputs['VORTICITY'].values}
        # Write vorticities to files
        vortxs = np.array(list(vort.values()))[:, 0]
        vortys = np.array(list(vort.values()))[:, 1]
        vortzs = np.array(list(vort.values()))[:, 2]
        vortx_f.write(','.join(map(str, vortxs)) + '\n')
        vorty_f.write(','.join(map(str, vortys)) + '\n')
        vortz_f.write(','.join(map(str, vortzs)) + '\n')


