from ..utils.heuristics import select_unassigned_variable, order_domain_values
from ..utils.utils import is_consistent, assign, unassign, assignment_in_grid
from ..utils.csp_formulation import SudokuCSP


def backtracking_search(csp):
    return backtrack({}, csp)


def backtrack(assignment, csp):
    if len(assignment) == len(csp.vars):
        return assignment

    var = select_unassigned_variable(assignment, csp)

    for value in order_domain_values(assignment, csp, var):
        if is_consistent(assignment, csp, var, value):
            assign(assignment, csp, var, value)

            result = backtrack(assignment, csp)
            if result:
                return result

        unassign(assignment, csp, var)

    return None


def solver_backtracking_for_csp(sudoku_grid):
    csp = SudokuCSP(sudoku_grid)

    csp.ac_3()  # pre-processing step

    return assignment_in_grid(backtracking_search(csp))
