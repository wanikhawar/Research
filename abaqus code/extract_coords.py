inp = open('NLPFEH_COUPLED_01MS_T350-fluid_domain.inp', 'r')
coords_file = open('GD0p1_coords.csv', 'w')

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

nodes = [node.replace(' ', '').replace('\n', '').split(',') for node in nodal_data]

num_nodes = len(nodes)

for node in nodes:
        coords_file.write("{0},{1},{2}\n".format(node[1], node[2], node[3]))

coords_file.close()
inp.close()