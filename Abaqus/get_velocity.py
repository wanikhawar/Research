# extracts velocity data from an ODB file and writes it to two files, velocity_x.dat and velocity_y.dat

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
with open('velocity_x.dat', 'w+') as vx_f, open('velocity_y.dat', 'w+') as vy_f:
    # Iterate over frames in 'flow' step
    for i in range(start_frame, len(fs)):
        # Create dictionary of node labels and x and y velocities
        vel = {velocity.nodeLabel: velocity.data[:2] for velocity in fs[i].fieldOutputs['V'].values}
        # Write velocities to files
        velxs = np.array(list(vel.values()))[:, 0]
        velys = np.array(list(vel.values()))[:, 1]
        vx_f.write(','.join(map(str, velxs)) + '\n')
        vy_f.write(','.join(map(str, velys)) + '\n')


