from __future__ import annotations
from amhe.evolution.network import Network
from typing import List
from copy import deepcopy
import numpy as np
import math
from random import randint


class Chromosome:
    def __init__(self, chrom: List, network: Network, rng, aggregated_demands: bool = False):
        self.chromosome: List = deepcopy(chrom)
        self.network: Network = network
        self.rng = rng
        self._cost = -1
        self._aggregated_demands = aggregated_demands

    def __lt__(self, other: Chromosome) -> bool:
        lt = self.number_of_visits() < other.number_of_visits()
        return lt

    def fill_random(self) -> None:
        if self._aggregated_demands:
            for d in self.network.demands.values():
                supply = self._get_aggregated_distribution(vector_length=len(d.paths), vector_sum=float(d.capacity))
                self.chromosome.append(supply)
        else:
            for d in self.network.demands.values():
                supply = self._get_dirichlet_distribution(vector_lenght=len(d.paths), vector_sum=float(d.capacity))
                self.chromosome.append(supply)

    def _get_aggregated_distribution(self, vector_length: int, vector_sum: float) -> List:
        result = [0.0 for i in range(vector_length)]
        result[self.rng.integers(low=0, high=len(result) - 1)] = vector_sum
        return result

    def _get_dirichlet_distribution(self, vector_lenght: int, vector_sum: float, scaling_factor: float = 1) -> List:
        '''
        scaling factor: > 0, variance is inversely proportional
        '''
        dirichlet_vec = self.rng.dirichlet(
            np.ones(vector_lenght) * scaling_factor)
        dirichlet_vec = np.rint(dirichlet_vec * vector_sum)
        return dirichlet_vec

    def cross(self, other: Chromosome) -> Chromosome:
        cross_mask = self.rng.choice(
            a=[True, False],
            size=len(self.chromosome))
        descendent1 = []
        descendend2 = []

        # not sure how to do it numpy way
        for i, gen1, gen2 in zip(cross_mask, self.chromosome, other.chromosome):
            if i:
                descendent1.append(gen1)
                descendend2.append(gen2)
            else:
                descendent1.append(gen2)
                descendend2.append(gen1)

        # it should be only one but should it be better?
        return Chromosome(descendent1, self.network, self.rng)

    def mutate(self, mutation_chance: float) -> None:
        '''
        mutation chance between 0 and 1
        '''
        # choose right
        # scaling_factor = self.number_of_visits()
        if self._aggregated_demands:
            for gene in self.chromosome:
                if self.rng.random() < mutation_chance:
                    capacity = sum(gene)
                    gene = self._get_aggregated_distribution(vector_length=len(gene), vector_sum=capacity)
        else:
            scaling_factor = 1
            for gene in self.chromosome:
                if self.rng.random() < mutation_chance:
                    capacity = sum(gene)
                    gene = self._get_dirichlet_distribution(len(gene), capacity, scaling_factor)

    def number_of_visits(self) -> int:

        edges_numer = self.network.net.number_of_edges()
        edges = [0.0 for _ in range(edges_numer)]

        assert(len(self.network.demands.values()) == len(self.chromosome))

        for demand, gen in zip(self.network.demands.values(), self.chromosome):

            assert(len(demand.paths) == len(gen))
            for gen_index, gen_elem in enumerate(gen):
                for path in demand.paths[gen_index]:
                    if edges[self.network.find_index(path[0], path[1])] < gen_elem:
                        edges[self.network.find_index(
                            path[0], path[1])] = gen_elem

        # for i in range(len(self.chromosome)):
        #     for j in range(len(self.chromosome[i])):
        #         for edge in self.network.demands[i].paths[j]:
        #             if edges[self.network.find_index(int(edge[0]), int(edge[1]))] < float(self.chromosome[i][j]):
        #                 edges[self.network.find_index(int(edge[0]), int(edge[1]))] = float(
        #                     self.chromosome[i][j])

        number_of_systems = 0
        for edge in edges:
            number_of_systems += math.ceil(edge/self.network.modularity)
        self._cost = number_of_systems
        return number_of_systems
