import itertools
import matplotlib.pyplot as plt
import networkx as nx
import numpy.random as rnd


class Europe:
    def __init__(self):
        self.graph = nx.read_edgelist("graph.txt")  # создание графа по списку ребер из файла
        self.graph.add_node('Malta')
        self.graph.add_node('Iceland')  # добавляю островные государства
        self.graph.add_node('Cyprus')
        self.nodes_number = self.graph.number_of_nodes()
        self.edges_number = self.graph.number_of_edges()
        subgraphs = list(nx.connected_components(self.graph))
        nodes_list = {}
        for subgraph in subgraphs:
            if len(subgraph) > len(nodes_list):
                nodes_list = subgraph
        self.largest_connected_component = nx.subgraph(self.graph, nodes_list)

    def number_of_nodes(self):
        print("Number of nodes:", self.nodes_number)

    def number_of_edges(self):
        print("Number of edges:", self.edges_number)

    def degree(self):
        array_degree_node = nx.degree(self.largest_connected_component)  # массив степеней всех вершин
        min_degree = self.nodes_number + 1
        max_degree = 0
        for node in array_degree_node:
            if node[1] < min_degree:
                min_degree = node[1]
            if node[1] > max_degree:
                max_degree = node[1]
        print("Minimum degree:", min_degree)
        print("Maximum degree:", max_degree)

    def diameter(self):
        print("Diameter:", nx.diameter(self.largest_connected_component))

    def center(self):
        print("Center:", nx.center(self.largest_connected_component))

    def radius(self):
        print("Radius:", nx.radius(self.largest_connected_component))

    def girth(self):
        subgraphs = list(nx.minimum_cycle_basis(self.largest_connected_component))
        nodes_list = self.nodes_number * [0]
        for subgraph in subgraphs:
            if len(subgraph) < len(nodes_list):
                nodes_list = subgraph
        print("Girth:", len(nodes_list))
