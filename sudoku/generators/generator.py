import numpy as np
from random import choice
from ..utils import N, flatten_position, objective_grid, available_nums
from ..solvers import solver_backtracking


# Returns a new sudoku game grid
def generator(difficulty=41):  # the difficulty parameter represents the number of initial sudoku clues
    grid = np.zeros((N, N), dtype='int8')

    actions = [None] * 81
    size = 0  # represents the grid fill level and the current position to be inserted
    while not objective_grid(grid):
        # Getting the next possible actions
        nums = available_nums(grid, *flatten_position(size))

        if nums:
            random_move = np.random.randint(len(nums))
            num = nums.pop(random_move)

            actions[size] = nums
        else:
            size -= 1

            while not actions[size]:  # undoing each modification to generate the next successor
                # It is not necessary to check if size == 0, as it will always be possible to generate a valid grid
                grid[flatten_position(size, inverted=True)] = 0
                size -= 1

            random_move = np.random.randint(len(actions[size]))
            num = actions[size].pop(random_move)

        grid[flatten_position(size, inverted=True)] = num
        size += 1

    while np.count_nonzero(grid) > difficulty:
        position = choice([(y, x) for y, x in zip(*np.where(grid))])  # (y, x) represents the ndarray manipulation order

        grid_copy = grid.copy()
        grid_copy[position] = 0

        if np.all(solver_backtracking(grid_copy)):  # checks if grid_copy has a unique solution
            grid[position] = 0

    return grid
