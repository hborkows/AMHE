from amhe.evolution.chromosome import Chromosome
from amhe.evolution.network import Network
import numpy as np
from typing import List


class Agent:
    def __init__(self, population_size=10) -> None:
        self.poputation_size = population_size
        self.rng = np.random.default_rng(6969)

    def init_population(self, network: Network) -> List:
        population = [Chromosome([], network, self.rng)
                      for _ in range(self.poputation_size)]
        return population

    def do_evolution(self):
        pass
