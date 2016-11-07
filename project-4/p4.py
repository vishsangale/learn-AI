"""
CS440 - Introduction to artificial intelligence
Assignment #4
Vishwanath Sangale
eID- vishsang
CSUID 830435005
"""

import csp
from utils import *
import time


class Knights(csp.CSP):
    def __init__(self, k, n):
        # print "Subclass object created."
        self.numberOfKnights = k
        self.dimensionOfTheBoard = n
        self.vars = range(2 * k)
        self.domains = csp.UniversalDict([(x, y) for x in range(n) for y in range(n)])
        self.neighbours = csp.UniversalDict(range(2 * k))
        # print self.vars
        # print self.domains
        csp.CSP.__init__(self,
                         self.vars,  # vars
                         self.domains,  # domains
                         self.neighbours,  # neighbours
                         self.knight_constraint)  # constraints

    def knight_constraint(self, A, a, B, b):
        """Constraint is satisfied (true) if A, B are really the same variable,
        or if they are not in the same row, down diagonal, or up diagonal."""
        if a == b:
            return False
        if (A == B) or (A < self.numberOfKnights <= B) or (A >= self.numberOfKnights > B):
            return True
        else:
            moves = ((-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1))
            ls = [(a[0] + move[0], a[1] + move[1]) for move in moves]
            if b in ls:
                return False
            else:
                return True


def backtracking_solve(k, n):
    """Backtracking with the best combination of heuristics."""
    print "Solve the problem using backtracking."
    """problem = Knights(k, n)
    t0 = time.time()
    print csp.backtracking_search(problem)
    print time.time() - t0"""

    problem = Knights(k, n)
    print "MRV"
    t0 = time.time()
    print csp.backtracking_search(problem, select_unassigned_variable=csp.mrv)
    print time.time() - t0

    problem = Knights(k, n)
    print "LCV"
    t0 = time.time()
    print csp.backtracking_search(problem, order_domain_values=csp.lcv)
    print time.time() - t0

    problem = Knights(k, n)
    print "MRV + LCV"
    t0 = time.time()
    print csp.backtracking_search(problem, select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv)
    print time.time() - t0

    problem = Knights(k, n)
    print "Forward Checking"
    t0 = time.time()
    print csp.backtracking_search(problem, inference=csp.forward_checking)
    print time.time() - t0

    problem = Knights(k, n)
    print "MRV + Forward Checking"
    t0 = time.time()
    print csp.backtracking_search(problem, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
    print time.time() - t0

    problem = Knights(k, n)
    print "LCV + Forward Checking"
    t0 = time.time()
    print csp.backtracking_search(problem, order_domain_values=csp.lcv, inference=csp.forward_checking)
    print time.time() - t0

    problem = Knights(k, n)
    print "MRV + LCV + Forward Checking"
    t0 = time.time()
    print csp.backtracking_search(problem, select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv,
                                  inference=csp.forward_checking)
    print time.time() - t0


def AC3_solve(k, n):
    """Solve the problem using AC3."""
    # print "Solve the problem using AC3."
    problem = Knights(k, n)
    t0 = time.time()
    solution = csp.AC3(problem)
    # print problem.domains
    print time.time() - t0
    return solution


def combined_solve(k, n):
    """Combines AC3 with backtracking search."""
    problem = Knights(k, n)
    print "Combined solve"
    t0 = time.time()
    csp.AC3(problem)
    # print problem.vars
    # print problem.neighbours
    # print problem.domains
    print time.time() - t0
    solution = csp.backtracking_search(problem)
    print time.time() - t0
    return solution
