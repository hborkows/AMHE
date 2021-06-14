import networkx
from amhe.evolution.chromosome import Chromosome
from amhe.evolution.network import Network
from amhe.evolution.agent import Agent
from typing import Sized
from mock import Mock
import numpy as np


class TestChromosome:
    def test_dirichlet_distribution(self):
        lenght = 5
        sum = 29
        rng = np.random.default_rng(6969)
        network = Mock(Network)
        chromosome = Chromosome([], network, rng)
        vec = chromosome._get_dirichlet_distribution(lenght, sum)
        real_sum = np.sum(vec)
        assert (sum == real_sum)

    def test_agent(self):
        network = Network(modularity=2)
        network.load_network("amhe/data/polska.xml")
        agent = Agent()
        chrom = agent.do_evolution(network)
        print(chrom)
        assert(False, str(chrom))
