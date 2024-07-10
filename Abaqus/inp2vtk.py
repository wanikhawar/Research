# Script to convert inp file to vtk file

# Number of DMD modes considered
r_dmd = 7
# Number of SVD modes considered
r_pod = 10


def status(string):
    print("-" * 30)
    print(string)


def write_start(vtk):
    vtk.write("# vtk DataFile Version 3.0\n")
    vtk.write("Mesh Data Information\n")
    vtk.write("ASCII\n")
    vtk.write("DATASET UNSTRUCTURED_GRID\n\n")


inp = open('input_file.inp', 'r')
vtk_v = open('vtk_velocity_file.vtk', 'w')
vtk_p = open('vtk_pressure_file.vtk', 'w')
vtk_vort = open('vtk_vorticity_file.vtk', 'w')


vtk_files = [vtk_v, vtk_p, vtk_vort]

for file in vtk_files:
    write_start(file)

# READ DATA FROM INP FILE
status("READING INP FILE")

lines = inp.readlines()

# CREATING A LIST OF COORDINATES
nodal_data = []

nodal_flag = False
for i in range(len(lines)):
    if nodal_flag:
        nodal_data.append(lines[i])
    if lines[i] == '*Node\n':
        nodal_flag = True
    if lines[i] == '*Element, type=FC3D8\n':
        nodal_flag = False
        nodal_data.remove('*Element, type=FC3D8\n')


status("WRITING COORDINATES TO VTK")

nodes = [node.replace(' ', '').replace('\n', '').split(',') for node in nodal_data]

num_nodes = len(nodes)

for file in vtk_files:
    file.write("POINTS {} float\n".format(num_nodes))


for node in nodes:
    for file in vtk_files:
        file.write("{0} {1} {2}\n".format(node[1], node[2], node[3]))

# CONNECTIVITY
conn_data = []

conn_flag = False
for i in range(len(lines)):
    if conn_flag:
        conn_data.append(lines[i])
    if '*Element' in lines[i]:
        conn_flag = True
    if "*Nset" in lines[i]:
        conn_flag = False

status("WRITING ELEMENT CONNECTIVITY DATA TO VTK")

elements = [connectivity.replace(' ', '').replace('\n', '').split(',') for connectivity in conn_data[:-1]]

num_elem = len(elements)

for file in vtk_files:
    file.write("\nCELLS {0} {1}\n".format(num_elem, num_elem * 9))

# SUBTRACT ONE FROM EACH NODE NUMBER TO START THE NUMBERING FROM ZERO
for element in elements:
    for file in vtk_files:
        file.write(
            "8 {0} {1} {2} {3} {4} {5} {6} {7}\n".format(eval(element[1]) - 1, eval(element[2]) - 1, eval(element[3]) - 1,
                                                         eval(element[4]) - 1, eval(element[5]) - 1,
                                                         eval(element[6]) - 1, eval(element[7]) - 1, eval(element[8]) - 1))

status("WRITING CELL TYPE TO VTK")

for file in vtk_files:
    file.write('\n')
    file.write("CELL_TYPES {}\n".format(num_elem))

for i in range(len(elements)):
    for file in vtk_files:
        file.write("12\n")

status("WRITING VELOCITY POD MODAL DATA TO VTK")
for file in vtk_files:
    file.write('\nPOINT_DATA {}\n'.format(num_nodes))


def read_write_POD(datafileName, vtk, r_pod, name):
    print("READING", name, "POD MODAL DATA")
    print("-" * 30)
    with open(datafileName, 'r') as pod_data:
        pod_raw = pod_data.readlines()
    pod_loc = [pod_row.replace(' ', '').replace('\n', '').split(',') for pod_row in pod_raw]

    print("WRITING", name, "POD MODAL DATA TO VTK")
    print("-" * 30)
    for mode in range(r_pod):
        mode_str = '{:02d}'.format(mode + 1)
        vtk.write('\nSCALARS ' + name + '_POD_mode_{} float 1\n'.format(mode_str))
        vtk.write('LOOKUP_TABLE default\n')
        vtk.write('\n'.join([node[mode] for node in pod_loc]))


def read_write_dmd(datafileName, vtk, r_dmd, name):
    print("READING", name, "DMD MODAL DATA")
    print("-" * 30)
    with open(datafileName, 'r') as dmd_data:
        dmd_raw = dmd_data.readlines()
    dmd_loc = [dmd_row.replace(' ', '').replace('\n', '').split(',') for dmd_row in dmd_raw]

    print("WRITING", name, "DMD MODAL DATA TO VTK")
    print("-" * 30)

    for mode in range(r_dmd):
        mode_str = '{:02d}'.format(mode + 1)
        vtk.write('\nSCALARS '+name+'_DMD_mode_{} float 1\n'.format(mode_str))
        vtk.write('LOOKUP_TABLE default\n')
        vtk.write('\n'.join([node[mode] for node in dmd_loc]))


read_write_POD('vx_pod_modes.csv', vtk_v, r_pod, 'vx')
read_write_POD('vy_pod_modes.csv', vtk_v, r_pod, 'vy')
read_write_POD('vmag_pod_modes.csv', vtk_v, r_pod, 'vmag')

read_write_POD('p_pod_modes.csv', vtk_p, r_pod, 'p')

read_write_POD('vortx_pod_modes.csv', vtk_vort, r_pod, 'vortx')
read_write_POD('vorty_pod_modes.csv', vtk_vort, r_pod, 'vorty')
read_write_POD('vortz_pod_modes.csv', vtk_vort, r_pod, 'vortz')
read_write_POD('vortmag_pod_modes.csv', vtk_vort, r_pod, 'vortmag')

read_write_dmd('vx_dmd_modes.csv', vtk_v, r_dmd, 'vx')
read_write_dmd('vy_dmd_modes.csv', vtk_v, r_dmd, 'vy')
read_write_dmd('vmag_dmd_modes.csv', vtk_v, r_dmd, 'vmag')
read_write_dmd('p_dmd_modes.csv', vtk_p, r_dmd, 'p')
read_write_dmd('vortx_dmd_modes.csv', vtk_vort, r_dmd, 'vortx')
read_write_dmd('vorty_dmd_modes.csv', vtk_vort, r_dmd, 'vorty')
read_write_dmd('vortz_dmd_modes.csv', vtk_vort, r_dmd, 'vortz')
read_write_dmd('vortmag_dmd_modes.csv', vtk_vort, r_dmd, 'vortmag')

for file in vtk_files:
    file.close()

inp.close()
