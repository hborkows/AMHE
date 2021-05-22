from amhe.evolution.agent import Agent

if __name__ == "__main__":
    agent = Agent()
    chrom = agent.do_evolution()
    print(chrom)
