from amhe.evolution.agent import Agent
from amhe.evolution.network import Network

if __name__ == "__main__":
    network = Network(modularity=2)
    network.load_network("/home/vm/studia/amhe/amhe/data/polska.xml")
    agent = Agent(population_size=10, max_lt_epsilon_allowed=1000, mutation_chance=0.5)
    chrom = agent.do_evolution(network)
    print(chrom.number_of_visits())
