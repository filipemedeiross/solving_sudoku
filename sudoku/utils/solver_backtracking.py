import numpy as np
from .problem_formulation import objective_grid, available_pos, available_nums


def solver_backtracking(grid):
    grid = grid.copy()  # does not change the original grid

    solution = None

    steps = np.count_nonzero(grid == 0)

    moves = [None] * steps
    actions = [None] * steps
    size = 0
    while True:
        if objective_grid(grid):
            if not np.all(solution):  # defines the solution, if no one has been found so far
                solution = grid.copy()
            else:  # if there is more than one solution, return None
                return None

        if size == steps or not available_nums(grid, *available_pos(grid)[0]):
            size -= 1

            while not actions[size]:
                if size == 0:
                    return solution

                grid[moves[size]] = 0
                size -= 1

            num = actions[size].pop()

            grid[moves[size]] = num
            size += 1

        pos = available_pos(grid)[0]
        nums = available_nums(grid, *pos)

        if nums:
            num = nums.pop()

            grid[pos] = num
            moves[size] = pos
            actions[size] = nums
            size += 1
