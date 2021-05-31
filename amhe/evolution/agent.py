from amhe.evolution.chromosome import Chromosome
from amhe.evolution.network import Network
import numpy as np
from typing import List


class Agent:
    def __init__(self, population_size: int = 10, mutation_chance: float = 0.05,
                 epsilon: float = 0.001, max_lt_epsilon_allowed: int = 10, aggregated_demands: bool = False,
                 seed: int = 69692502):
        self._poputation_size = population_size
        self._rng = np.random.default_rng(seed)
        self._population: List[Chromosome] = []
        self._mutation_chance = mutation_chance
        self._epsilon = epsilon
        self._max_lt_epsilon_allowed = max_lt_epsilon_allowed
        self._aggregated_demands = aggregated_demands

    def _init_population(self, network: Network):
        self._population = [Chromosome([], network, self._rng, self._aggregated_demands)
                            for _ in range(self._poputation_size)]
        for chrom in self._population:
            chrom.fill_random()

    def _do_mutate(self):
        for specimen in self._population:
            specimen.mutate(self._mutation_chance)

    def _do_cross(self):  # should be in place on self._population object
        i = 0
        children = []
        while i < len(self._population) - 1:
            children.append(self._population[i].cross(self._population[i + 1]))
            i += 1
        new_population = self._population + children
        new_population.sort()
        new_population = new_population[:self._poputation_size]
        self._population = new_population

    def _select_new_population(self):
        self._do_mutate()
        self._do_cross()

    def _find_best_in_population(self):
        result = self._population[0]
        for specimen in self._population:
            if specimen < result:
                result = specimen
        return result
    # Returns best chromosome

    def do_evolution(self, network: Network, max_repeats: int = 10000, mode: str = 'best', colname: str = 'best_result'):
        self._init_population(network)

        result_list = []
        i = 0
        lt_epsilon_count = 0
        best_so_far = self._find_best_in_population()
        best_result_so_far = best_so_far.number_of_visits()

        while i < max_repeats:
            best_from_current = self._find_best_in_population()
            best_result_from_current = best_from_current.number_of_visits()

            if best_from_current < best_so_far:
                best_so_far = best_from_current

            if abs(best_result_so_far - best_result_from_current) <= self._epsilon:
                lt_epsilon_count += 1
            else:
                lt_epsilon_count = 0

            if lt_epsilon_count >= self._max_lt_epsilon_allowed:
                if mode == 'best':
                    return best_so_far
                elif mode == 'partial':
                    return result_list

            best_result_so_far = best_so_far.number_of_visits()

            if mode == 'partial':
                result_dict = {
                    'generation': i,
                    colname: best_result_so_far
                }
                result_list.append(result_dict)
            #print(f'Generation number: {i}')
            #print(f'Best result: {best_result_so_far}')
            i += 1
            self._select_new_population()

        if mode == 'best':
            return best_so_far
        elif mode == 'partial':
            return result_list
