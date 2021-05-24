from amhe.evolution.agent import Agent
from amhe.evolution.network import Network

if __name__ == "__main__":
    network = Network(modularity=2)
    network.load_network("data/polska.xml")
    agent = Agent()
    chrom = agent.do_evolution(network)
    print(chrom)
