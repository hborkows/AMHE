from __future__ import annotations
from amhe.evolution.network import Network
from typing import List
from copy import deepcopy
import numpy as np
import math


class Chromosome:
    def __init__(self, chrom: List, network: Network, rng: np.Generator):
        self.chrom: List = deepcopy(chrom)
        self.network: Network = network
        self.rng = rng 

    def fill_random(self):       
        for d in self.network.demands:
            supply = self._get_dirichlet_distribution(vector_lenght=d.paths, vector_sum=d.capacity)
            self.chrom.append(supply)

    def _get_dirichlet_distribution(self, vector_lenght: int, vector_sum: int) -> List:
        dirichlet_vec = self.rng.dirichlet(np.ones(vector_lenght))
        dirichlet_vec = np.rint(dirichlet_vec * vector_sum)
        return dirichlet_vec

    def cross(self, other: Chromosome) -> Chromosome:
        cross_mask = self.rng.choice(
            a=[True, False],
            size=len(self.chrom))
        descendent1 = []
        descendend2 = [] 

        #not sure how to do it numpy way
        for i, gen1, gen2 in zip(cross_mask, self.chrom, other.chrom):
            if i:
                descendent1.append(gen1)
                descendend2.append(gen2)
            else:
                descendent1.append(gen2)
                descendend2.append(gen1)

        #it should be only one but should it be better?    
        return Chromosome(descendent1, self.network)

    def mutate(self, mutation_chance):
        pass

    def number_of_visits(self) -> int:
        edges_numer = self.network.net.number_of_edges()
        edges = [0 for _ in range(edges_numer)]

        for i in range(len(self.chrom)):
            for j in range (len(self.chrom[i])):
                for edge in self.network.demands[i].paths[j]:
                    if self.network.option == 0:
                        if edges[self.network.findIndex(int(edge[0]), int(edge[1]))] < float(self.chrom[i][j]):
                            edges[self.network.findIndex(int(edge[0]), int(edge[1]))] = float(self.chrom[i][j])
                    else:
                        edges[self.network.findIndex(int(edge[0]), int(edge[1]))] += float(self.chrom[i][j])

        numberOfSystems = 0
        for edge in edges:
            numberOfSystems += math.ceil(edge/self.network.modularity)
        return numberOfSystems
