from amhe.evolution.demand import Demand
from typing import List, Dict
import networkx as nx
from xml.etree import ElementTree


class Network:
    def __init__(self, modularity: int):
        self.modularity: int = modularity
        self.nodes: Dict[str: int] = {}
        self.demands: Dict[int: Demand] = {}
        self.net: nx.Graph = nx.Graph()
        self.link_ids: List[int] = []

    def _add_node(self, node: str):
        index = self.net.number_of_nodes()
        self.nodes[node] = index
        self.net.add_node(index, name=node)

    def _add_edge(self, start_node, end_node, capacity):
        start_index = self.nodes[start_node]
        end_index = self.nodes[end_node]
        self.net.add_edge(start_index, end_index, c1=start_index, c2=end_index,
                          capacity=capacity, systems=capacity//self.modularity)


    def _add_demand(self, id: int, capacity: int, paths: List):
        demand: Demand = Demand(id, capacity)
        for path in paths:
            demand.add_path(path)
        self.demands[id] = demand

    def load_network(self, filename: str):
        tree = ElementTree.parse(filename)
        root = tree.getroot()

        # read cities - nodes in graph
        for child in root[0][0]:
            for k, v in child.attrib.items():
                self._add_node(v)

        edges = []
        for child in root[0][1]:
            self._add_edge(child[0].text, child[1].text, 0)
            edges.append((self.nodes[child[0].text], self.nodes[child[1].text]))

            for k, v in child.attrib.items():
                self.link_ids.append(v)

        for child in root[1]:
            paths = []
            for links in child[3]:
                path = []
                for link in links:
                    path.append(edges[self.link_ids.index(link.text)])
                paths.append(path)
            for k, v in child.attrib.items():
                self._add_demand(v, child[2].text, paths)

    def find_index(self, index1, index2):
        counter = 0
        for edge in self.net.edges:
            if (edge[0] == index1 and edge[1] == index2) or (edge[0] == index2 and edge[1] == index1):
                return counter
            counter += 1
