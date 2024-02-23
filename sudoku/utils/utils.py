import numpy as np
from .constants import N


def assign(assignment, csp, var, value):
    assignment[var] = value

    # Making inferences
    for neighbor in csp.neighbors[var]:
        if value in csp.domains[neighbor]:
            csp.domains[neighbor].remove(value)
            csp.cuts[var].append((neighbor, value))

def unassign(assignment, csp, var):
    del assignment[var]

    # Unmaking inferences
    for neighbor, value in csp.cuts[var]:
        csp.domains[neighbor].append(value)

    csp.cuts[var].clear()

def assignment_in_grid(assignment):
    if not assignment:
        return assignment

    grid = np.zeros((N, N), dtype='int8')

    for pos, value in assignment.items():
        grid[pos] = value

    return grid

def process_grid(grid):
    return [(j, i, grid[j, i])
            for j in range(N)
            for i in range(N)]
