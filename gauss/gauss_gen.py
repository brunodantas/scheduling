import sys

t1_weight = 0
graph_size = 0

def makegraph():
	layer_qty = graph_size
	vertex_qty = ((graph_size + 1) * (graph_size + 2))//2 - 1
	layers = dict()
	edge_qty = graph_size * (graph_size + 2) - 3
	vertices = [x for x in range(vertex_qty)]

	first_layer_size = graph_size + 1
	for i in range(layer_qty):
		layers[i] = []
		for j in range(first_layer_size - i):
			v = vertices.pop(0)
			layers[i].append(v)	

	weights = dict()
	edge_weights = dict()
	w0 = ([1] + [2*x for x in range(1,graph_size)]) [::-1]
	wn = ([1] + [x for x in range(1,graph_size)]) [::-1]

	for l in range(layer_qty):
		for v in layers[l]:
			weights[v] = wn[l]
		weights[ layers[l][0] ] = w0[l]

	edges = []

	v1 = layers[0][0]
	for v2 in layers[0][1::]:
		edges.append((v1,v2))
		edge_weights[v1,v2] = 12
	for i in range(1,len(layers[0])):
		v1 = layers[0][i]
		v2 = layers[1][i-1]
		edges.append((v1,v2))
		edge_weights[v1,v2] = 8

	for l in range(1,layer_qty-1):
		v1 = layers[l][0]
		for v2 in layers[l][1::]:
			edges.append((v1,v2))
			edge_weights[v1,v2] = 12
		v2 = layers[l+1][0]
		edges.append((v1,v2))
		edge_weights[v1,v2] = 12

		for i in range(1,len(layers[l])):
			v1 = layers[l][i]
			v2 = layers[l+1][i-1]
			edges.append((v1,v2))
			edge_weights[v1,v2] = 8

	v1 = layers[layer_qty-1][0]
	v2 = layers[layer_qty-1][1]
	edges.append((v1,v2))
	edge_weights[v1,v2] = 12

	txt_file = "gauss{}.txt".format(vertex_qty)
	dot_file = "gauss{}.dot".format(vertex_qty)
	png_file = "gauss{}.png".format(vertex_qty)

	file = open(txt_file,'w')
	print("generating {}".format(txt_file))
	for v in range(vertex_qty):
		file.write("{}\n".format(weights[v]))

	file.write("{}\n".format(edge_qty))
	for v1,v2 in edges:
		file.write("{} {} {}\n".format(v1,v2,edge_weights[(v1,v2)]))
	file.close()

	file = open(dot_file,'w')
	print("generating {}".format(dot_file))
	file.write("digraph G{\n\tsplines=polyline\n\tnodesep=0.5\n\tranksep=0.8")

	for v in range(vertex_qty):
		file.write("\tv{} [label = \"T{}\\n{}\"]\n".format(v,v,weights[v]))
	file.write("\n")

	for v1,v2 in edges:
		s = "\tv{} -> v{} ".format(v1,v2)
		if edge_weights[(v1,v2)] == 8:
			s += "[style=dashed]"
		file.write("{}\n".format(s))

	i = 0
	for l in range(layer_qty):
		s = "\t{rank = same; "
		for v in layers[l]:
			s += "v" + str(v) + "; "
		s += '}'
		file.write("{}\n".format(s))

	file.write("}")
	file.close()

	import subprocess
	print("generating {}".format(png_file))
	bashCommand = "dot -Tpng {} -o {}".format(dot_file,png_file)
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()

	bashCommand = "rm {}".format(dot_file)
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()

if __name__ == '__main__':
	graph_size = int(sys.argv[1])
	t1_weight = 2*(graph_size-1)
	makegraph()