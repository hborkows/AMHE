from amhe.evolution.demand import Demand
from typing import List
import networkx as nx
from xml.etree import ElementTree


class Network:
    def __init__(self, modularity: int):
        self.modularity: int = modularity
        self.nodes: List[str] = []
        self.demands: List[Demand] = []
        self.net: nx.Graph = nx.Graph()
        self.link_ids: List[int] = []

    def _add_node(self, node: str):
        self.nodes.append(node)
        self.net.add_node(self.net.number_of_nodes(), name=node)

    def _add_edge(self, start_node, end_node, capacity):
        start_index = self.nodes.index(start_node)
        end_index = self.nodes.index(end_node)
        self.net.add_edge(start_index, end_index, c1=start_index, c2=end_index, capacity=capacity, systems=capacity//self.modularity)

    def _add_demand(self, id: int, capacity: int, paths: List):
        demand: Demand = Demand(id, capacity)
        for path in paths:
            demand.add_path(path)
        self.demands.append(demand)

    def load_network(self, filename: str):
        tree = ElementTree.parse(filename)
        root = tree.getroot()

        for child in root[0][0]: # read cities - nodes in graph
            for k, v in child.attrib.items():
                self._add_node(v)

        edges = []
        for child in root[0][1]:
            self._add_edge(child[0].text, child[1].text, 0)
            edges.append((self.nodes.index(child[0].text), self.nodes.index(child[1].text)))
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
