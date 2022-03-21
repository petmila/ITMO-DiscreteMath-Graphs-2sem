import itertools
import matplotlib.pyplot as plt
import networkx as nx
import numpy.random as rnd
import haversine

class Europe:
    def __init__(self):
        self.graph = nx.read_edgelist("graph.txt")  # создание графа по списку ребер из файла(файл есть в репозитории)
        self.graph.add_node('Malta')
        self.graph.add_node('Iceland')  # добавляю островные государства
        self.graph.add_node('Cyprus')

        self.nodes_number = self.graph.number_of_nodes()
        self.edges_number = self.graph.number_of_edges()

        subgraphs = list(nx.connected_components(self.graph))
        self.connected_nodes_list = {}
        for subgraph in subgraphs:
            if len(subgraph) > len(self.connected_nodes_list):
                self.connected_nodes_list = subgraph
        self.largest_connected_component = nx.subgraph(self.graph, self.connected_nodes_list)

        self.degree = nx.degree(self.largest_connected_component)  # массив степеней всех вершин
        min_degree = self.nodes_number + 1
        max_degree = 0
        for node in self.degree:
            if node[1] < min_degree:
                min_degree = node[1]
            if node[1] > max_degree:
                max_degree = node[1]
        self.min_degree = min_degree
        self.max_degree = max_degree

        self.v_coloring = nx.greedy_color(self.largest_connected_component) # множество пар (вершина : номер цвета)
        
        self.dual = nx.line_graph(self.largest_connected_component) # создание дуального графа
        self.e_coloring = nx.greedy_color(self.dual)

        cliques = list(nx.find_cliques(self.largest_connected_component))
        self.max_clique = cliques[0]
        for clique in cliques:
            if len(self.max_clique) < len(clique):
                self.max_clique = clique
            
        self.max_stable_set = nx.maximal_independent_set(self.largest_connected_component)
        # для невзвешенного графа данная функция сочтет вес дефолтным - 1
        # так что она посчитает просто количество ребер
        self.max_matching = nx.max_weight_matching(self.largest_connected_component)
        self.v_cover = nx.approximation.min_weighted_vertex_cover(self.largest_connected_component)
        self.e_cover = nx.min_edge_cover(self.largest_connected_component)

        self.blocks = list(nx.biconnected_components(self.graph))


    def number_of_nodes(self):
        print("Number of nodes:", self.nodes_number)

    def number_of_edges(self):
        print("Number of edges:", self.edges_number)

    def degree(self):
        print("Minimum degree:", self.min_degree)
        print("Maximum degree:", self.max_degree)

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
    
    def vertex_coloring(self):
        print("Minimum vertex coloring:", max(self.v_coloring.values()))

    def edge_coloring(self):
        print("Minimum edge coloring:", max(self.e_coloring.values()))

    def maximum_clique(self):
        print("Maximum clique:", self.max_clique)

    def maximum_stable_set(self):
        print("Maximum stable set:", self.max_stable_set)

    def maximum_matching(self):
        print("Maximum matching:", self.max_matching)

    def minimum_vertex_cover(self):
        print("Minimum vertex cover:", self.v_cover)
    
    def minimum_edge_cover(self):
        print("Minimum edge cover:", self.e_cover)

    def shortest_closed_walk_vertexes(self):
        self.tsp = (nx.algorithms.approximation.traveling_salesman_problem(self.largest_connected_component))
        print("Shortest closed walk, which visits every vetrex:\n")
        i = 0
        while i < (len(self.tsp) - 4):
            print(self.tsp[i], (self.tsp[i], self.tsp[i + 1]),
            self.tsp[i + 1], (self.tsp[i + 1], self.tsp[i + 2]),
            self.tsp[i + 2], (self.tsp[i + 2], self.tsp[i + 3]),
            self.tsp[i + 3], (self.tsp[i + 3], self.tsp[i + 4]))
            i += 4
        print(self.tsp[len(self.tsp) - 1])

    def shortest_closed_walk_edges(self):
        print("List of vertexes of the shortest closed walk, which visits every edge:\n",
        nx.eulerian_circuit(self.largest_connected_component))

    def all_blocks(self):
        print("Biconnected components:")
        for item in self.blocks:
            print(item)

    def all_2_edge_connected_components(self):
        print("2-edge-connected components:")
        for item in list(nx.biconnected_component_edges(self.graph)):
            print(item)

    def make_weighted_graph(self):
        self.weighted_graph = nx.read_edgelist("graph.txt")  # создание графа по списку ребер из файла(файл есть в репозитории)
        self.weighted_graph.add_node('Malta')
        self.weighted_graph.add_node('Iceland')  # добавляю островные государства
        self.weighted_graph.add_node('Cyprus')

        nx.set_node_attributes(self.weighted_graph, geolock)
        edges_weight = {}
        for item in nx.edges(self.weighted_graph):
            edges_weight[item] = int(haversine.haversine((self.weighted_graph.nodes[item[0]]["height"], self.weighted_graph.nodes[item[0]]["width"]),
            (self.weighted_graph.nodes[item[1]]["height"],self.weighted_graph.nodes[item[1]]["width"])))
        nx.set_edge_attributes(self.weighted_graph , edges_weight, 'weight')

        self.largest_weighted_connected_component = nx.subgraph(self.weighted_graph, self.connected_nodes_list)
    def spanning_tree(self):
        self.minimum_spanning_tree = nx.minimum_spanning_tree(self.largest_weighted_connected_component)
        print("Minimum_spanning_tree:")
        return self.minimum_spanning_tree
    
    def prufer(self):
        print("Prufer code:", nx.to_prufer_sequence(nx.convert_node_labels_to_integers(self.minimum_spanning_tree)))