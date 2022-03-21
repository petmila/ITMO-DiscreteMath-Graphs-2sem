import itertools
import matplotlib.pyplot as plt
import networkx as nx
import numpy.random as rnd
import geopy.distance as dist

#graph = nx.Graph()
graph = nx.read_edgelist("graphs.txt") 
graph.add_node('c')

subgraphs = list(nx.connected_components(graph))
nodes_list = {}
for subgraph in subgraphs:
    if len(subgraph) > len(nodes_list):
        nodes_list = subgraph
largest_connected_component = nx.subgraph(graph, nodes_list)

array_degree_node = nx.degree(largest_connected_component)
# массив степеней всех вершин
min_degree = graph.number_of_nodes() + 1
max_degree = 0
for node in array_degree_node:
    if node[1] < min_degree:
        min_degree = node[1]
    if node[1] > max_degree:
        max_degree = node[1]
print("Minimum degree:", min_degree)
print("Maximum degree:", max_degree)

print("Diameter:", nx.diameter(largest_connected_component))
print("Center:", nx.center(largest_connected_component))
print("Radius:", nx.radius(largest_connected_component))

subgraphs = list(nx.minimum_cycle_basis(largest_connected_component))
nodes_list = graph.number_of_nodes()*[0]
for subgraph in subgraphs:
    if len(subgraph) < len(nodes_list):
        nodes_list = subgraph
print("Girth:", len(nodes_list))

blocks = list(nx.biconnected_components(graph))
print("Biconnected components:")
for item in blocks:
    print(item)
print("2-edge-connected components:")
for item in list(nx.biconnected_component_edges(graph)):
    print(item)