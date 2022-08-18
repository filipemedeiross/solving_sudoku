# For better documentation see tests/sudoku_solver.ipynb


import numpy as np
from .problem_formulation import N, STEP, square_loc, objective_grid


class SudokuCSP:
    def __init__(self, grid):
        self.domains = self.node_consistency(grid)

        self.neighbors = self.generate_neighbors()  # avoid checking each time it is necessary

        # Similar difference constraints, so attribute contains only the scopes
        self.constraints = [(var, neighbor) for var in self.vars for neighbor in self.neighbors[var]]

        self.cuts = {var: [] for var in self.vars}

    @staticmethod
    def node_consistency(grid):
        domains = {(y, x): [grid[y, x]] if grid[y, x] else list(range(1, N + 1))
                   for y in range(N)
                   for x in range(N)}

        return domains

    def generate_neighbors(self):
        neighbors = {(y, x): set([(y, i) for i in range(N) if i != x] +
                                 [(j, x) for j in range(N) if j != y] +
                                 [(j, i) for j in range(*square_loc(y)) for i in range(*square_loc(x))
                                  if i != x and j != y])
                     for y, x in self.vars}

        return neighbors

    def ac_3(self):
        queue = self.constraints.copy()

        while queue:
            xi, xj = queue.pop(0)

            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False

                for xk in self.neighbors[xi] - {xj}:
                    queue.append((xk, xi))

        return True

    def revise(self, xi, xj):
        revised = False

        for x in self.domains[xi]:
            if not any([x != y for y in self.domains[xj]]):
                self.domains[xi].remove(x)

                revised = True

        return revised

    @property
    def vars(self):
        return list(self.domains.keys())

    @property
    def won(self):
        if all(len(domain) == 1 for domain in self.domains.values()):
            return objective_grid(np.array([domain[0] for domain in self.domains.values()]).reshape((N, N)))

        return False