import sys
import math

node_weight = 60
edge_weight = 80
graph_size = 0

def makegraph():
	vertex_qty = 2*graph_size - 1 + graph_size * int(math.log(graph_size,2))
	hlayer_qty = int(math.log(graph_size,2))
	layer_qty = 1 + 2*hlayer_qty
	edge_qty = 2*graph_size - 2 + 2*graph_size * int(math.log(graph_size,2))
	layers = dict()

	#first half nodes
	node_id = 0
	node_qty = 1
	for i in range(hlayer_qty + 1):
		layers[i] = []
		for j in range(node_qty):
			layers[i].append(node_id)
			node_id += 1
		node_qty *= 2

	#second half nodes
	node_qty = graph_size
	for i in range(hlayer_qty+1,layer_qty):
		layers[i] = []
		for j in range(graph_size):
			layers[i].append(node_id)
			node_id += 1

	#first half edges:
	edges = []
	for l in range(hlayer_qty):
		for i,x in enumerate(layers[l]):
			y1 = layers[l+1][2*i]
			y2 = layers[l+1][2*i+1]
			edges.append((x,y1))
			edges.append((x,y2))

	#second half edges:
	n = 1
	dist = 1
	for l in range(hlayer_qty,layer_qty-1):
		for i,x in enumerate(layers[l]):
			y1 = layers[l+1][i]
			y2 = layers[l+1][i+dist] if i % (2*dist) < dist else layers[l+1][i-dist]
			y = [(x,y1),(x,y2)]
			y.sort()
			edges += y
		dist *= 2

	txt_file = "fft{}.txt".format(vertex_qty)
	dot_file = "fft{}.dot".format(vertex_qty)
	png_file = "fft{}.png".format(vertex_qty)

	file = open(txt_file,'w')
	print("generating {}".format(txt_file))
	for v in range(vertex_qty):
		file.write("{}\n".format(node_weight))

	file.write("{}\n".format(edge_qty))
	for v1,v2 in edges:
		file.write("{} {} {}\n".format(v1,v2,edge_weight))
	file.close()

	file = open(dot_file,'w')
	print("generating {}".format(dot_file))
	file.write("digraph G{\nsplines=false;\tnodesep=0.5\n\tranksep=1\n")

	for v in range(vertex_qty):
		file.write("\tv{} [label = \"T{}\"]\n".format(v,v,node_weight))
	file.write("\n")

	for v1,v2 in edges:
		s = "\tv{} -> v{} ".format(v1,v2)
		file.write("{}\n".format(s))

	for l in range(1,layer_qty):
		s = "\t{rank = same; "
		for v in layers[l][:-1]:
			s += "v" + str(v) + " -> "
		s += "v" + str(layers[l][-1]) + " "

		s += '[ style=invis ]; rankdir = LR;}'
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
	graph_size = 2 ** int(sys.argv[1])
	makegraph()