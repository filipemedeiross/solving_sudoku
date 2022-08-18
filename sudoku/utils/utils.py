# Auxiliary functions


import numpy as np
from .problem_formulation import N


def is_consistent(assignment, csp, var, value):
    for current_var, current_value in assignment.items():
        if current_value == value and current_var in csp.neighbors[var]:
            return False

    return True


def assign(assignment, csp, var, value):
    assignment[var] = value

    # Making inferences
    for neighbor in csp.neighbors[var]:
        if value in csp.domains[neighbor] and neighbor not in assignment.keys():
            csp.domains[neighbor].remove(value)

            csp.cuts[var].append((neighbor, value))


def unassign(assignment, csp, var):
    if var in assignment.keys():
        # Unmaking inferences
        for neighbor, value in csp.cuts[var]:
            csp.domains[neighbor].append(value)

        csp.cuts[var].clear()

        del assignment[var]


def assignment_in_grid(assignment):
    if not assignment:  # if the fetch fails, the conversion returns None
        return assignment

    grid = np.zeros((N, N))

    for pos, value in assignment.items():
        grid[pos] = value

    return grid
