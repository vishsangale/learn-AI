"""
Fall 2014 - Introduction to artificial intelligence
Vishwanath Sangale
"""
import search
import time


class MAXSAT(search.Problem):
    def __init__(self, file_name):
        """

        :type file_name: object
        """
        input_file = open(file_name, 'r')

        for line in input_file:
            print line
        self.initial = ()

    def actions(self, state):
        print state

    def result(self, state, action):
        print state, action


def run_max_sat():
    problem = MAXSAT("uuf50-0331.cnf")

    output_file = open('maxsat_results.txt', 'w+')
    # t0 = time.time()
    # search.hill_climbing(problem)
    # total = time.time() - t0
    # print total
    t0 = time.time()
    search.simulated_annealing(problem)
    total = time.time() - t0
    print total
    t0 = time.time()
    search.genetic_search(problem)
    total = time.time() - t0
    print total
    output_file.close()

if __name__ == "__main__":
    run_max_sat()
