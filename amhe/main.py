from amhe.evolution.agent import Agent
from amhe.evolution.network import Network
from multiprocessing import Pool
import itertools
import pandas as pd
from datetime import datetime


def timer(start_time=None):
    if not start_time:
        start_time = datetime.now()
        return start_time
    elif start_time:
        thour, temp_sec = divmod((datetime.now() - start_time).total_seconds(), 3600)
        tmin, tsec = divmod(temp_sec, 60)
        print('\n Time taken: %i hours %i minutes and %s seconds.' % (thour, tmin, round(tsec, 2)))


def run_params_test(params):
    print(f'Doing run with params: {params}')
    mutation_chance = params[0]
    population_size = params[1]
    network = Network(modularity=10)
    network.load_network("/home/vm/studia/amhe/amhe/data/polska.xml")
    agent = Agent(population_size=population_size, max_lt_epsilon_allowed=10, mutation_chance=mutation_chance)
    chrom = agent.do_evolution(network)
    result = {
        'result': chrom.number_of_visits(),
        'params': params
    }
    return result


def best_params(n_jobs, params_list):
    pool = Pool(n_jobs)
    results = pool.map(run_params_test, params_list)
    pool.close()
    pool.join()
    result_df = pd.DataFrame(results)
    # return result_df
    return result_df[result_df['result'] == result_df['result'].min()]


if __name__ == "__main__":
    mutation_chances = [0.1, 0.01, 0.05, 0.001, 0.005]
    population_sizes = [2, 10, 20]
    params = itertools.product(mutation_chances, population_sizes)

    start_time = timer()
    print(best_params(n_jobs=6, params_list=params))
    timer(start_time)
    '''
    print(chrom.number_of_visits())'''
