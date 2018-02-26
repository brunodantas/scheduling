import sys

t1_weight = 80
edge_weight = 40
graph_size = 0

def makegraph():
	layer_qty = 2*graph_size - 1
	vertex_qty = graph_size ** 2
	layers = dict()
	edge_qty = 2 * graph_size * (graph_size-1)
	vertices = [x for x in range(vertex_qty)]
	for i in range(graph_size):
		layers[i] = []
		for j in range(i+1):
			v = vertices.pop(0)
			layers[i].append(v)

	for i in range(graph_size,layer_qty):
		layers[i] = []
		for j in range(layer_qty-i):
			v = vertices.pop(0)
			layers[i].append(v)

	# print(layers)

	weights = dict()
	weights[0] = [t1_weight]
	weights[1] = 2*[t1_weight+10]
	for i in range(2,graph_size-1):
		weights[i] = [weights[i-1][0]]
		for j in range(1,i):
			weights[i].append(t1_weight+20)
		weights[i].append(weights[i][0])

	weights[graph_size-1] = [t1_weight]
	for j in range(1,graph_size-1):
		weights[graph_size-1].append(t1_weight+20)
	weights[graph_size-1].append(t1_weight)

	for i in range(1,graph_size):
		weights[i+graph_size-1] = weights[graph_size-1-i]

	# print(weights)
	txt_file = "laplace{}.txt".format(vertex_qty)
	dot_file = "laplace{}.dot".format(vertex_qty)
	png_file = "laplace{}.png".format(vertex_qty)

	file = open(txt_file,'w')
	print("generating {}".format(txt_file))
	for l in range(layer_qty):
		for w in weights[l]:
			file.write("{}\n".format(w))
	file.write("{}\n".format(edge_qty))
	for l in range(layer_qty/2):
		for i,v in enumerate(layers[l]):
			file.write("{} {} {}\n".format(v,layers[l+1][i],edge_weight))
			file.write("{} {} {}\n".format(v,layers[l+1][i+1],edge_weight))

	for l in range(layer_qty/2,layer_qty-1):
		file.write("{} {} {}\n".format(layers[l][0],layers[l+1][0],edge_weight))
		file.write("{} {} {}\n".format(layers[l][-1],layers[l+1][-1],edge_weight))
		for i,v in enumerate(layers[l][1:-1]):
			file.write("{} {} {}\n".format(v,layers[l+1][i],edge_weight))
			file.write("{} {} {}\n".format(v,layers[l+1][i+1],edge_weight))
	file.close()

	file = open(dot_file,'w')
	print("generating {}".format(dot_file))
	file.write("digraph G{\nsplines=false;\n")
	i = 0
	for l in range(layer_qty):
		for w in weights[l]:
			file.write("\tv{} [label = \"T{}\\n{}\"]\n".format(i,i,w))
			i += 1
	file.write("\n")
	for l in range(layer_qty/2):
		for i,v in enumerate(layers[l]):
			file.write("\tv{} -> v{}\n".format(v,layers[l+1][i]))
			file.write("\tv{} -> v{}\n".format(v,layers[l+1][i+1]))
			# file.write("\tv{} -> v{} [label = \"{}\"]\n".format(v,layers[l+1][i],edge_weight))
			# file.write("\tv{} -> v{} [label = \"{}\"]\n".format(v,layers[l+1][i+1],edge_weight))

	for l in range(layer_qty/2,layer_qty-1):
		file.write("\tv{} -> v{}\n".format(layers[l][0],layers[l+1][0]))
		file.write("\tv{} -> v{}\n".format(layers[l][-1],layers[l+1][-1]))
		# file.write("\tv{} -> v{} [label = \"{}\"]\n".format(layers[l][0],layers[l+1][0],edge_weight))
		# file.write("\tv{} -> v{} [label = \"{}\"]\n".format(layers[l][-1],layers[l+1][-1],edge_weight))
		for i,v in enumerate(layers[l][1:-1]):
			file.write("\tv{} -> v{}\n".format(v,layers[l+1][i]))
			file.write("\tv{} -> v{}\n".format(v,layers[l+1][i+1]))
			# file.write("\tv{} -> v{} [label = \"{}\"]\n".format(v,layers[l+1][i],edge_weight))
			# file.write("\tv{} -> v{} [label = \"{}\"]\n".format(v,layers[l+1][i+1],edge_weight))
	file.write("}")
	file.close()

	import subprocess
	print("generating {}".format(png_file))
	bashCommand = "dot -Tpng laplace{}.dot -o laplace{}.png".format(vertex_qty,vertex_qty)
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()

	bashCommand = "rm {}".format(dot_file)
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()

if __name__ == '__main__':
	graph_size = int(sys.argv[1]) + 1
	makegraph()
