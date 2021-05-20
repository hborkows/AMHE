from typing import Sized
from amhe.evolution.chromosome import Chromosome


from amhe.evolution.chromosome import Chromosome
import numpy as np


class TestChromosome:
    def test_dirichlet_distribution(self):
        lenght = 5
        sum = 29
        rng = np.random.default_rng(6969)
        chromosome = Chromosome([], None, rng)
        vec = chromosome._get_dirichlet_distribution(lenght, sum)
        real_sum = np.sum(vec)
        assert (sum == real_sum)
