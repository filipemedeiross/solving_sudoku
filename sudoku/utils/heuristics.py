# Implementing the functions that apply the heuristics


# Implementing the least constraining value heuristics
def least_constraining_value(assignment, csp, var, value):
    return len([neighbor
                for neighbor in csp.neighbors[var]
                if neighbor not in assignment and value in csp.domains[neighbor]])


def select_unassigned_variable(assignment, csp):
    available_vars = [var
                      for var in csp.vars
                      if var not in assignment.keys()]

    # mrv heuristic in the key parameter chooses the variable with the smallest legal value
    return min(available_vars, key=lambda var: len(csp.domains[var]))


def order_domain_values(assignment, csp, var):
    return sorted(csp.domains[var], key=lambda value: least_constraining_value(assignment, csp, var, value))
