from __future__ import annotations
from amhe.evolution.network import Network
from typing import List
from copy import deepcopy


class Chromosome:
    def __init__(self, chrom: List, network: Network):
        self.chrom: List = deepcopy(chrom)
        self.network: Network = network

    def cross(self, other: Chromosome) -> Chromosome:
        pass

    def mutate(self, mutation_chance):
        pass

    def number_of_visits(self) -> int:
        pass
