from amhe.evolution.chromosome import Chromosome
from amhe.evolution.network import Network
import numpy as np
from typing import List


class Agent:    
    def __init__(self, population_size: int = 10, mutation_chance: float = 0.05):
        self._poputation_size = population_size
        self._rng = np.random.default_rng(6969)
        self._population: List[Chromosome] = []
        self._mutation_chance = mutation_chance

    def _init_population(self, network: Network):
        #check for pep standard layout
        self._population = [Chromosome([], network, self._rng) for _ in range(self._poputation_size)]

    def _do_mutate(self):
        for specimen in self._population:
            specimen.mutate(self._mutation_chance)

    def _do_cross(self):  # should be in place on self._population object
        pass

    def _select_new_population(self):
        self._do_mutate()
        self._do_cross()

    def do_evolution(self, network: Network, max_repeats: int = 10000):
        self._init_population(network)

        i = 0
        finish = False
        while i < max_repeats and not finish:
            i += 1



