from amhe.evolution.chromosome import Chromosome
from amhe.evolution.network import Network
import numpy as np
from typing import List


class Agent:
    def __init__(self, population_size: int = 10, mutation_chance: float = 0.05,
                 epsilon: float = 0.001, max_lt_epsilon_allowed: int = 10):
        self._poputation_size = population_size
        self._rng = np.random.default_rng(6969)
        self._population: List[Chromosome] = []
        self._mutation_chance = mutation_chance
        self._epsilon = epsilon
        self._max_lt_epsilon_allowed = max_lt_epsilon_allowed

    def _init_population(self, network: Network):
        self._population = [Chromosome([], network, self._rng)
                            for _ in range(self._poputation_size)]
        for chrom in self._population:
            chrom.fill_random()

    def _do_mutate(self):
        for specimen in self._population:
            specimen.mutate(self._mutation_chance)

    def _do_cross(self):  # should be in place on self._population object
        pass

    def _select_new_population(self):
        self._do_mutate()
        self._do_cross()

    # Returns best chromosome
    def do_evolution(self, network: Network, max_repeats: int = 10000) -> Chromosome:
        self._init_population(network)
        self._population.sort()

        i = 0
        lt_epsilon_count = 0
        best_so_far = self._population[0]
        best_result_so_far = best_so_far.number_of_visits()

        while i < max_repeats:
            best_from_current = self._population[0]
            best_result_from_current = best_from_current.number_of_visits()

            if best_from_current < best_so_far:
                best_so_far = best_from_current

            if abs(best_result_so_far - best_result_from_current) <= self._epsilon:
                lt_epsilon_count += 1
            else:
                lt_epsilon_count = 0

            if lt_epsilon_count >= self._max_lt_epsilon_allowed:
                return best_so_far

            best_result_so_far = best_so_far.number_of_visits()
            i += 1
            self._select_new_population()
            self._population.sort()

        return best_so_far
