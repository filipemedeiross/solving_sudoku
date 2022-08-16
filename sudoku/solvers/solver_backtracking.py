import numpy as np
from ..utils import objective_grid, available_pos, available_nums


def solver_backtracking(sudoku_grid):
    grid = sudoku_grid.copy()  # does not change the original grid

    solution = None

    max_steps = np.count_nonzero(grid == 0)
    moves = [None] * max_steps
    actions = [None] * max_steps

    size = 0
    while True:
        if objective_grid(grid):
            if not np.all(solution):  # defines the solution, if no one has been found so far
                solution = grid.copy()
            else:  # if there is more than one solution, return None
                return None

        # size == max_steps works like not available_pos(grid)
        while size == max_steps or not available_nums(grid, *available_pos(grid)[0]):
            size -= 1

            while not actions[size]:
                # There are no more possibilities for actions to be explored
                if size == 0:
                    return solution  # single solution or None

                x, y = moves[size]
                grid[y, x] = 0  # undoing each modification to generate the next successor
                size -= 1

            x, y = moves[size]
            num = actions[size].pop()

            grid[y, x] = num
            size += 1

        # Developing subtrees:
        # not at the search limit
        # there are actions available for the current tree level
        x, y = available_pos(grid)[0]
        nums = available_nums(grid, x, y)
        num = nums.pop()

        grid[y, x] = num
        moves[size] = (x, y)
        actions[size] = nums
        size += 1
